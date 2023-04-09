package main

import (
	"uav-rest-api/web"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/authenticate", web.authenticate)
	// REST API endpoints
	router.GET("/connect", web.ConnectHandler)
	router.GET("/getAllTasks", web.GetAllTasksHandler)
	router.GET("/getAllMissions", web.GetAllMissionsHandler)
	router.GET("/GetTaskHistory", web.GetTaskHistoryHandler)
	router.GET("/GetMssionHistory", web.GetMissionHistoryHandler)

	router.POST("/createTask", web.CreateTaskHandler)
	router.POST("/createMission", web.CreateMissionHandler)
	router.POST("/TaskResultTransaction", web.TaskResultTransactionHandler)

	router.DELETE("/DeleteTaskByID", web.DeleteTaskByIDHandler)
	router.DELETE("/DeleteMissionByID", web.DeleteMissionByIDHandler)


	router.Run(":3030")
}
