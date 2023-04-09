/*
Copyright 2021 IBM All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
*/

package web

import (
	"bytes"
	"crypto/x509"
	"encoding/json"
	"fmt"
	"os"
	"path"
	"time"
	"net/http"
	"io/ioutil"
	"net"

	"github.com/gin-gonic/gin"
	"github.com/hyperledger/fabric-gateway/pkg/client"
	"github.com/hyperledger/fabric-gateway/pkg/identity"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

type ConnectionInfo struct {
	TLSCertPath   string `json:"tlsCertPath"`
	GatewayPeer   string `json:"gatewayPeer"`
	PeerEndpoint  string `json:"peerEndpoint"`
	CertPath      string `json:"certPath"`
	MSPID         string `json:"mspID"`
	KeyPath       string `json:"keyPath"`
}

// Asset describes basic details of what makes up a simple asset
type TASK_Asset struct {
	ID        		string  `json:"id"`
	Name    		string  `json:"name"`
	MissionID    	string  `json:"mission_id"`
	TaskID    		string  `json:"task_id"`
	Latitude  		string 	`json:"latitude"`
	Longitude 		string 	`json:"longitude"`
	Comments    	string  `json:"comments"`
}

type Mission_Asset struct {
	ID      	string  	`json:"id"`
	Comments    string  	`json:"comments"`
	AssetIDs 	[]string 	`json:"asset_ids"`
}

type RequestPayload struct {
	Auth 		ConnectionInfo 	`json:"auth"`
	TASK 		TASK_Asset 		`json:"Task_Asset"`
	Mission 	Mission_Asset 	`json:"Mission_Asset"`
}

type UAVData struct {
	Latitude    string 			`json:"latitude"`
	Longitude   string 			`json:"longitude"`
	UAVManager  string 			`json:"uav_manager"`
	MissionID   string  		`json:"mission_id"`
	TaskID   	string 			`json:"task_id"`
	Host  		string 			`json:"host"`
	Auth  		ConnectionInfo 	`json:"auth"`
}

type TaskIDResponse struct {
	TaskID 	string `json:"task_id"`
	Lat 	string `json:"latitude"`
	Lon 	string `json:"longitude"`
}

func authenticate(c *gin.Context) {
	var payload RequestPayload
	
	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
    // 인증 정보를 사용하여 인증 파일을 생성합니다.
	wallet, err := gateway.NewFileSystemWallet("wallet")
	if err != nil {
		return fmt.Errorf("Failed to create wallet: %v", err)
	}

	err = ioutil.WriteFile("cert.pem", []byte(payload.Auth.CertPath), 0644)
	if err != nil {
		return fmt.Errorf("Failed to write certificate file: %v", err)
	}

	err = ioutil.WriteFile("key.pem", []byte(payload.Auth.KeyPath), 0644)
	if err != nil {
		return fmt.Errorf("Failed to write key file: %v", err)
	}

	identity, err := createIdentity(payload.Auth.MSPID, "cert.pem", "key.pem")
	if err != nil {
		return fmt.Errorf("Failed to create identity: %v", err)
	}

	err = wallet.Put(payload.Auth.MSPID, identity)
	if err != nil {
		return fmt.Errorf("Failed to put identity into wallet: %v", err)
	}

	// Add the TLS cert for the gateway peer
	tlsCert, err := ioutil.ReadFile(payload.Auth.TLSCertPath)
	if err != nil {
		return fmt.Errorf("Failed to read tlsCertPath: %v", err)
	}

	gatewayConfig := &gateway.GatewayConfig{
		Identity:      payload.Auth.MSPID,
		Wallet:        wallet,
		PeerEndpoint:  payload.Auth.PeerEndpoint,
		GatewayPeer:   payload.Auth.GatewayPeer,
		TLSRootCert:   tlsCert,
	}

	err = gateway.Init(gatewayConfig)
	if err != nil {
		return fmt.Errorf("Failed to initialize gateway: %v", err)
	}

	return nil
}


	
func createGatewayConnection(payload RequestPayload) (*client.Gateway, error) {
	clientConnection := newGrpcConnection(payload.Auth.TLSCertPath, payload.Auth.GatewayPeer, payload.Auth.PeerEndpoint)

	id := newIdentity(payload.Auth.CertPath, payload.Auth.MSPID)
	sign := newSign(payload.Auth.KeyPath)

	// Create a Gateway connection for a specific client identity
	gw, err := client.Connect(
		id,
		client.WithSign(sign),
		client.WithClientConnection(clientConnection),
		// Default timeouts for different gRPC calls
		client.WithEvaluateTimeout(5*time.Second),
		client.WithEndorseTimeout(15*time.Second),
		client.WithSubmitTimeout(5*time.Second),
		client.WithCommitStatusTimeout(1*time.Minute),
	)

	return gw, err
}

// newGrpcConnection creates a gRPC connection to the Gateway server.
func newGrpcConnection(tlsCertPath string, gatewayPeer string, peerEndpoint string) *grpc.ClientConn {
	certificate, err := loadCertificate(tlsCertPath)
	if err != nil {
		panic(err)
	}

	certPool := x509.NewCertPool()
	certPool.AddCert(certificate)
	transportCredentials := credentials.NewClientTLSFromCert(certPool, gatewayPeer)

	connection, err := grpc.Dial(peerEndpoint, grpc.WithTransportCredentials(transportCredentials))
	if err != nil {
		panic(fmt.Errorf("failed to create gRPC connection: %w", err))
	}

	return connection
}

// newIdentity creates a client identity for this Gateway connection using an X.509 certificate.
func newIdentity(certPath string, mspID string) *identity.X509Identity {
	certificate, err := loadCertificate(certPath)
	if err != nil {
		panic(err)
	}

	id, err := identity.NewX509Identity(mspID, certificate)
	if err != nil {
		panic(err)
	}

	return id
}

func loadCertificate(filename string) (*x509.Certificate, error) {
	certificatePEM, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read certificate file: %w", err)
	}
	return identity.CertificateFromPEM(certificatePEM)
}

// newSign creates a function that generates a digital signature from a message digest using a private key.
func newSign(keyPath string) identity.Sign {
	files, err := os.ReadDir(keyPath)
	if err != nil {
		panic(fmt.Errorf("failed to read private key directory: %w", err))
	}
	privateKeyPEM, err := os.ReadFile(path.Join(keyPath, files[0].Name()))

	if err != nil {
		panic(fmt.Errorf("failed to read private key file: %w", err))
	}

	privateKey, err := identity.PrivateKeyFromPEM(privateKeyPEM)
	if err != nil {
		panic(err)
	}

	sign, err := identity.NewPrivateKeySign(privateKey)
	if err != nil {
		panic(err)
	}

	return sign
}

// Format JSON data
func formatJSON(data []byte) string {
	var prettyJSON bytes.Buffer
	if err := json.Indent(&prettyJSON, data, "", "  "); err != nil {
		panic(fmt.Errorf("failed to parse JSON: %w", err))
	}
	return prettyJSON.String()
}

func getHostAddress() (string, error) {
	interfaces, err := net.InterfaceAddrs()
	if err != nil {
		return "", err
	}

	for _, addr := range interfaces {
		ip, _, err := net.ParseCIDR(addr.String())
		if err != nil {
			continue
		}

		ipv4 := ip.To4()
		if ipv4 == nil {
			continue // Skip IPv6 addresses for now
		}

		if !ipv4.IsLoopback() && !ipv4.IsUnspecified() {
			return ipv4.String(), nil
		}
	}

	return "", fmt.Errorf("no valid host address found")
}

func sendRequestToUAVServer(url string, data UAVData) (string, error) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return "", err
	}

	request, err := http.NewRequest("PUT", url, bytes.NewReader(jsonData))
	if err != nil {
		return "", err
	}
	request.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return "", err
	}
	defer response.Body.Close()

	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}
/*
	Gateway - Asset
*/

// Evaluate a transaction to query ledger state.
func getAllTasks(contract *client.Contract) string {
	fmt.Println("\n--> Evaluate Transaction: GetAllAssets, function returns all the current assets on the ledger")

	evaluateResult, err := contract.EvaluateTransaction("GetAllTasks")
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	// Check if evaluateResult is empty
	if len(evaluateResult) == 0 {
		fmt.Println("No assets found on the ledger.")
		return "None Data"
	}
	result := formatJSON(evaluateResult)
	fmt.Printf("*** Result:%s\n", result)

	return result
}

func getAllMissions(contract *client.Contract) string {
	fmt.Println("\n--> Evaluate Transaction: GetAllAssets, function returns all the current assets on the ledger")

	evaluateResult, err := contract.EvaluateTransaction("GetAllMissions")
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	// Check if evaluateResult is empty
	if len(evaluateResult) == 0 {
		fmt.Println("No assets found on the ledger.")
		return "None Data"
	}
	result := formatJSON(evaluateResult)
	fmt.Printf("*** Result:%s\n", result)

	return result
}
// Evaluate a transaction by assetID to query ledger state.
func readTaskByID(contract *client.Contract, assetID string) {
	fmt.Printf("\n--> Evaluate Transaction: ReadAsset, function returns asset attributes\n")

	evaluateResult, err := contract.EvaluateTransaction("QueryUAV", assetID)
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	result := formatJSON(evaluateResult)

	fmt.Printf("*** Result:%s\n", result)
}

// Evaluate a transaction by assetID to query ledger state.
func deleteByID(contract *client.Contract, assetID string) {
	fmt.Printf("\n--> Evaluate Transaction: DeleteAsset\n")

	_, err := contract.SubmitTransaction("DeleteAsset", assetID)
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	fmt.Printf("*** Result:%s\n", "Deleted")
}

// Evaluate a transaction by assetID to query ledger state.
func createTask(contract *client.Contract, auth ConnectionInfo, mission_ID string, task_ID string, name string, latitude string, longitude string) {
	fmt.Printf("\n--> Evaluate Transaction: UpdatedAsset\n")

	_, err := contract.EvaluateTransaction("AssetExists", mission_ID)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}

	host, err := getHostAddress()
	if err != nil {
		fmt.Println("Error getting host address:", err)
	} else {
		fmt.Println("Host address:", host)
	}

	uavData := UAVData{
		Latitude:   latitude,
		Longitude:  longitude,
		UAVManager: name,
		TaskID: 	task_ID,
		MissionID:	mission_ID,
		Host: 		host,
		Auth:		auth,
	}

	uavServerURL := "http://192.168.72.130:8000/start_task/"
	response, err := sendRequestToUAVServer(uavServerURL, uavData)
	if err != nil {
		panic(fmt.Errorf("failed to send request to UAV server: %w", err))
	}
	fmt.Printf("*** UAV Server Response: %s\n", response)

	var taskIDResponse TaskIDResponse
	err = json.Unmarshal([]byte(response), &taskIDResponse)
	if err != nil {
		panic(fmt.Errorf("failed to unmarshal JSON response: %w", err))
	}

	taskID := taskIDResponse.TaskID
	lat := taskIDResponse.Lat
	lon := taskIDResponse.Lon

	fmt.Printf("*** UAV Server Response: %s %s\n", lat, lon)

	comments := fmt.Sprintf("(%s, %s)/Movement/Mission Delivery", latitude, longitude)

	_, err = contract.SubmitTransaction("CreateTask", task_ID, name, mission_ID, taskID, lat, lon, comments)
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	fmt.Printf("*** UAV Server Response: %s %s\n", mission_ID, task_ID)
	_, err = contract.SubmitTransaction("AddAssetToMission", mission_ID, task_ID)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}

	fmt.Printf("*** Transaction committed successfully\n")
}

// Evaluate a transaction by assetID to query ledger state.
func TaskResultTransaction(contract *client.Contract, mission_ID string, task_ID string, comments string, name string, taskID string, latitude string, longitude string) {
	fmt.Printf("\n--> Evaluate Transaction: Task Result Transaction\n")
	fmt.Printf("*** Result:%s\n%s\n%s\n%s\n%s\n%s\n%s\n", task_ID, name, mission_ID, taskID, latitude, longitude, comments)

	_, err := contract.SubmitTransaction("UpdateTask", task_ID, name, mission_ID, taskID, latitude, longitude, comments)
	if err != nil {
		fmt.Printf("*** Result:%w\n", err)
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	fmt.Printf("*** Result:%s\n", "updated")
}

// get Asset History
func getTaskHistory(contract *client.Contract, assetID string) (string, error) {

	evaluateResult, err := contract.EvaluateTransaction("GetTaskHistory", assetID)
	if err != nil {
		return "", fmt.Errorf("failed to evaluate transaction: %w", err)
	}

	result := formatJSON(evaluateResult)

	fmt.Printf("*** Result:%s\n", result)
	return result, nil
}


/*
	Gateway - Mission
*/


func createMission(contract *client.Contract, missionID string, comments string) {
	fmt.Printf("\n--> Submit Transaction: CreateMission \n")

	_, err := contract.SubmitTransaction("CreateMission", missionID, comments)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}

	fmt.Printf("*** Transaction committed successfully\n")
}

func addAssetToMission(contract *client.Contract, missionID string, assetID string) {
	fmt.Printf("\n--> Submit Transaction: AddAssetToMission \n")

	_, err := contract.SubmitTransaction("AddAssetToMission", missionID, assetID)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}

	fmt.Printf("*** Transaction committed successfully\n")
}

func readMissionByID(contract *client.Contract, missionID string) {
	fmt.Printf("\n--> Evaluate Transaction: QueryMission, function returns mission attributes\n")

	evaluateResult, err := contract.EvaluateTransaction("QueryMission", missionID)
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	result := formatJSON(evaluateResult)

	fmt.Printf("*** Result:%s\n", result)
}

func getMissionHistory(contract *client.Contract, missionID string) (string, error) {
	evaluateResult, err := contract.EvaluateTransaction("GetMissionHistory", missionID)
	if err != nil {
		return "", fmt.Errorf("failed to evaluate transaction: %w", err)
	}
	result := formatJSON(evaluateResult)

	fmt.Printf("*** Result:%s\n", result)
	return result, nil
}

/*
	REST request to gateway - ALL
*/


// Routing Handler
func ConnectHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

    c.Set("contract", contract)

    c.JSON(http.StatusOK, gin.H{"result": "Connected to the network"})
}

// Routing Handler
func GetAllTasksHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	result := getAllTasks(contract)
	
	c.Data(http.StatusOK, "application/json", []byte(result))
}

func GetAllMissionsHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	result := getAllMissions(contract)
	
	c.Data(http.StatusOK, "application/json", []byte(result))
}
/*
	REST request to gateway - Asset
*/

// Routing Handler
func ReadTaskByIDHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	readTaskByID(contract, payload.TASK.ID)
}

// Routing Handler
func GetTaskHistoryHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	jsonResult, err := getTaskHistory(contract, payload.TASK.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Set the Content-Type header to "application/json" and write the jsonResult string as response
	c.Data(http.StatusOK, "application/json", []byte(jsonResult))
}

// Routing Handler
func DeleteTaskByIDHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	deleteByID(contract, payload.TASK.ID)
}

// Routing Handler
func CreateTaskHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	createTask(contract, payload.Auth, payload.TASK.MissionID, payload.TASK.ID, payload.TASK.Name, payload.TASK.Latitude, payload.TASK.Longitude)
}

// Routing Handler
func TaskResultTransactionHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)
	TaskResultTransaction(contract, payload.TASK.MissionID, payload.TASK.ID, payload.TASK.Comments, payload.TASK.Name, payload.TASK.TaskID, payload.TASK.Latitude, payload.TASK.Longitude)
	deleteByID(contract, payload.TASK.ID)
}

/*
	REST request to gateway - Mission
*/

func CreateMissionHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()

	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	createMission(contract, payload.Mission.ID, payload.Mission.Comments)
}

// Routing Handler
func ReadMissionByIDHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	readMissionByID(contract, payload.Mission.ID)
}

// Routing Handler
func GetMissionHistoryHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	jsonResult, err := getMissionHistory(contract, payload.Mission.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Set the Content-Type header to "application/json" and write the jsonResult string as response
	c.Data(http.StatusOK, "application/json", []byte(jsonResult))
}

// Routing Handler
func DeleteMissionByIDHandler(c *gin.Context) {
	var payload RequestPayload

	if err := c.BindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	gw, err := createGatewayConnection(payload)
	if err != nil {
		panic(err)
	}
	defer gw.Close()


	// Override default values for chaincode and channel name as they may differ in testing contexts.
	chaincodeName := "basic"
	if ccname := os.Getenv("CHAINCODE_NAME"); ccname != "" {
		chaincodeName = ccname
	}

	channelName := "mychannel"
	if cname := os.Getenv("CHANNEL_NAME"); cname != "" {
		channelName = cname
	}

	network := gw.GetNetwork(channelName)
	contract := network.GetContract(chaincodeName)

	deleteByID(contract, payload.Mission.ID)
}
