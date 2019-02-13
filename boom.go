package main

import (
	"fmt"
	"encoding/json"
	//"boom/pb"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
	//"boom/shim"
)

type UserValue struct {
	IDCardNumber string `json:"IDCardNumber"`
}

type PropertyValue struct {
	TXID string `json:"TXID"`
}

// SimpleChaincode example simple Chaincode implementation
type SimpleChaincode struct {
}

func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Property_test_1 Init")
	_, args := stub.GetFunctionAndParameters()
	if len(args) != 0 {
		return shim.Error("Incorrect number of arguments. Expecting 0")
	}
	return shim.Success(nil)
}

func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Property_test_1 Invoke")
	function, args := stub.GetFunctionAndParameters()
	if function == "initUser" {
		return t.initUser(stub, args)
	} else if function == "initProperty" {
		return t.initProperty(stub, args)
	} else if function == "queryUser" {
		return t.queryUser(stub, args)
	} else if function == "queryProperty" {
		return t.queryProperty(stub, args)
	}

	return shim.Error("Invalid invoke function name. Expecting \"init\" \"invoke\" \"query\"")
}

func (t *SimpleChaincode) initUser(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var userKey string
	var idcardNumber string
	var err error

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	userKey = "User_" + args[0]
	idcardNumber = args[1]
	fmt.Printf("initUser: userKey: %s, IDcardNumber: %s\n", userKey, idcardNumber)
	state, err := stub.GetState(userKey)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if state == nil {
		stateStruct := UserValue{IDCardNumber:idcardNumber}
		newState, err := json.Marshal(stateStruct)
		if err != nil {
			return shim.Error("Failed to marshal old state")
		}
		err = stub.PutState(userKey, []byte(newState))
		if err != nil {
			return shim.Error(err.Error())
		}
	} else {
		return shim.Error("User already exists.")
	}
	return shim.Success(nil)
}

func (t *SimpleChaincode) initProperty(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var owner string
	var production string
	var txid string
	var err error

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	owner = args[0]
	production = args[1]
	txid = args[2]

	var productionKey = "Property_" + owner + "_" + production
	fmt.Printf("initProperty: Owner: %s, Production: %s, txid: %s\n", owner, production, txid)
	state, err := stub.GetState(productionKey)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if state == nil {
		stateStruct := PropertyValue{TXID:txid}
		newState, err := json.Marshal(stateStruct)
		if err != nil {
			return shim.Error("Failed to marshal old state")
		}
		err = stub.PutState(productionKey, []byte(newState))
		if err != nil {
			return shim.Error(err.Error())
		}
	} else {
		return shim.Error("Property already exists.")
	}
	return shim.Success(nil)
}

func (t *SimpleChaincode) queryUser(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var owner string // Entities
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to query")
	}

	owner = "User_" + args[0]

	// Get the state from the ledger
	Re_str, err := stub.GetState(owner)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + owner + "\"}"
		return shim.Error(jsonResp)
	}

	if Re_str == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + owner + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := Re_str
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Re_str)
}

func (t *SimpleChaincode) queryProperty(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var owner string
	var propertyHash string
	var err error

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting userID and propertyHash for query.")
	}

	owner = args[0]
	propertyHash = args[1]
	var productionKey = "Property_" + owner + "_" + propertyHash

	// Get the state from the ledger
	Re_str, err := stub.GetState(productionKey)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + productionKey + "\"}"
		return shim.Error(jsonResp)
	}

	if Re_str == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + productionKey + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := Re_str
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Re_str)
}

func main() {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}

