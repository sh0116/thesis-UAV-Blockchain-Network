package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// UAVControlChaincode provides functions for managing an Asset
type UAVControlChaincode struct {
	contractapi.Contract
}

type Mission_Asset struct {
	ID      	string  	`json:"id"`
	Comments    string  	`json:"comments"`
	AssetIDs 	[]string 	`json:"asset_ids"`
}

// Asset
type TASK_Asset struct {
	ID        	string  `json:"id"`
	Name    	string  `json:"name"`
	MissionID   string  `json:"missionid"`
	TaskID    	string  `json:"taskid"`
	Latitude  	string 	`json:"latitude"`
	Longitude 	string 	`json:"longitude"`
	Comments    string  `json:"comments"`
}

type MissionHistory struct {
	TxId        string  		`json:"txId"`
	Value       Mission_Asset 	`json:"value"`
	IsDelete    bool    		`json:"isDelete"`
	TxTimestamp string  		`json:"txTimestamp"`
}


type TaskHistory struct {
	TxId        string  	`json:"txId"`
	Value       TASK_Asset  `json:"value"`
	IsDelete    bool    	`json:"isDelete"`
	TxTimestamp string  	`json:"txTimestamp"`
}

// GetAllTasks는 world state에 저장된 모든 TASK_Asset을 반환합니다.
func (s *UAVControlChaincode) GetAllTasks(ctx contractapi.TransactionContextInterface) ([]*TASK_Asset, error) {
	taskIterator, err := ctx.GetStub().GetStateByRange("TASK", "TASK~")
	if err != nil {
		return nil, fmt.Errorf("failed to get tasks: %v", err)
	}
	defer taskIterator.Close()

	var tasks []*TASK_Asset
	for taskIterator.HasNext() {
		queryResponse, err := taskIterator.Next()
		if err != nil {
			return nil, fmt.Errorf("failed to get next task: %v", err)
		}

		var task TASK_Asset
		err = json.Unmarshal(queryResponse.Value, &task)
		if err != nil {
			return nil, fmt.Errorf("failed to unmarshal task: %v", err)
		}

		tasks = append(tasks, &task)
	}

	return tasks, nil
}

// GetAllMissions는 world state에 저장된 모든 Mission_Asset을 반환합니다.
func (s *UAVControlChaincode) GetAllMissions(ctx contractapi.TransactionContextInterface) ([]*Mission_Asset, error) {
	missionIterator, err := ctx.GetStub().GetStateByRange("MISSION", "MISSION~")
	if err != nil {
		return nil, fmt.Errorf("failed to get missions: %v", err)
	}
	defer missionIterator.Close()

	var missions []*Mission_Asset
	for missionIterator.HasNext() {
		queryResponse, err := missionIterator.Next()
		if err != nil {
			return nil, fmt.Errorf("failed to get next mission: %v", err)
		}

		var mission Mission_Asset
		err = json.Unmarshal(queryResponse.Value, &mission)
		if err != nil {
			return nil, fmt.Errorf("failed to unmarshal mission: %v", err)
		}

		missions = append(missions, &mission)
	}

	return missions, nil
}

/*
	Asset 
*/

// CreateAsset issues a new asset to the world state with given details.
func (s *UAVControlChaincode) CreateTask(ctx contractapi.TransactionContextInterface, id string, name string, missionid string, taskid string, latitude string, longitude string, comments string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

    asset := TASK_Asset{
        ID:            	id,
        Name:        	name,
		MissionID:		missionid,
		TaskID:			taskid,
        Latitude:       latitude,
        Longitude:      longitude,
		Comments:		comments,
    }
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// CreateAsset issues a new asset to the world state with given details.
func (s *UAVControlChaincode) UpdateTask(ctx contractapi.TransactionContextInterface, id string, name string, missionid string, taskid string, latitude string, longitude string, comments string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

    asset := TASK_Asset{
        ID:            	id,
        Name:        	name,
		MissionID:		missionid,
		TaskID:			taskid,
        Latitude:       latitude,
        Longitude:      longitude,
		Comments:		comments,
    }
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// QueryUAV returns the asset stored in the world state with given id.
func (s *UAVControlChaincode) QueryUAV(ctx contractapi.TransactionContextInterface, id string) (*TASK_Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset TASK_Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// DeleteAsset deletes an given asset from the world state.
func (s *UAVControlChaincode) DeleteAsset(ctx contractapi.TransactionContextInterface, id string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	return ctx.GetStub().DelState(id)
}

// AssetExists returns true when asset with given ID exists in world state
func (s *UAVControlChaincode) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

func (s *UAVControlChaincode) GetTaskHistory(ctx contractapi.TransactionContextInterface, id string) ([]*TaskHistory, error) {
	resultsIterator, err := ctx.GetStub().GetHistoryForKey(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get asset history for %s: %v", id, err)
	}
	defer resultsIterator.Close()

	var history []*TaskHistory
	for resultsIterator.HasNext() {
		response, err := resultsIterator.Next()
		if err != nil {
			return nil, fmt.Errorf("failed to read asset history from iterator: %v", err)
		}
	
		var asset TASK_Asset
		if !response.IsDelete {
			if err := json.Unmarshal(response.Value, &asset); err != nil {
				return nil, fmt.Errorf("failed to unmarshal asset: %v", err)
			}
		}
	
		txTimestamp := response.Timestamp.String()
	
		historyItem := &TaskHistory{
			TxId:        response.TxId,
			Value:       asset,
			IsDelete:    response.IsDelete,
			TxTimestamp: txTimestamp,
		}
		history = append(history, historyItem)
	}
	

	return history, nil
}


/*
	Mission 
*/

func (s *UAVControlChaincode) CreateMission(ctx contractapi.TransactionContextInterface, id string, comments string) error {
	exists, err := s.MissionExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the mission %s already exists", id)
	}

	mission := Mission_Asset{
		ID:      id,
		Comments:    comments,
		AssetIDs: make([]string, 0),
	}
	missionJSON, err := json.Marshal(mission)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, missionJSON)
}

func (s *UAVControlChaincode) AddAssetToMission(ctx contractapi.TransactionContextInterface, missionid string, taskid string) error {
	mission, err := s.QueryMission(ctx, missionid)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}
	_, err = s.AssetExists(ctx, taskid)
	if err != nil {
		return fmt.Errorf("failed to read from world state: %v", err)
	}

	mission.AssetIDs = append(mission.AssetIDs, taskid)
	missionJSON, err := json.Marshal(mission)
	if err != nil {
		return fmt.Errorf("failed : %v", err)
	}

	return ctx.GetStub().PutState(missionid, missionJSON)
}

func (s *UAVControlChaincode) QueryMission(ctx contractapi.TransactionContextInterface, id string) (*Mission_Asset, error) {
	missionJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if missionJSON == nil {
		return nil, fmt.Errorf("the mission %s does not exist", id)
	}

	var mission Mission_Asset
	err = json.Unmarshal(missionJSON, &mission)
	if err != nil {
		return nil, err
	}

	return &mission, nil
}

func (s *UAVControlChaincode) MissionExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	missionJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return missionJSON != nil, nil
}

func (s *UAVControlChaincode) GetMissionHistory(ctx contractapi.TransactionContextInterface, id string) ([]*MissionHistory, error) {
	resultsIterator, err := ctx.GetStub().GetHistoryForKey(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get mission history for %s: %v", id, err)
	}
	defer resultsIterator.Close()

	var history []*MissionHistory
	for resultsIterator.HasNext() {
		response, err := resultsIterator.Next()
		if err != nil {
			return nil, fmt.Errorf("failed to read mission history from iterator: %v", err)
		}
	
		var mission Mission_Asset
		if !response.IsDelete {
			if err := json.Unmarshal(response.Value, &mission); err != nil {
				return nil, fmt.Errorf("failed to unmarshal mission: %v", err)
			}
		}
	
		txTimestamp := response.Timestamp.String()
	
		historyItem := &MissionHistory{
			TxId:        response.TxId,
			Value:       mission,
			IsDelete:    response.IsDelete,
			TxTimestamp: txTimestamp,
		}
		history = append(history, historyItem)
	}
	
	return history, nil
}