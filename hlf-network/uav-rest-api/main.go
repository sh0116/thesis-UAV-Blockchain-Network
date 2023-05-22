package main

import (
    "net/http"
	"uav-rest-api/web"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
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


    // Replace these file paths with the paths to your own certificate and key files
    certFile := "ums_rest.crt"
    keyFile := "ums_rest.key"

	server := &http.Server{
        Addr:      ":3030",
        Handler:   router,
        TLSConfig: nil,
    }

    err := server.ListenAndServeTLS(certFile, keyFile)
    if err != nil {
        panic("Failed to start HTTPS server: " + err.Error())
    }
}