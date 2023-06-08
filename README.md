# thesis-UAV-Blockchain-Network
Design and Implementation of Multi-UAV Mission Management Method Based on Blockchain

# 블록체인 기반 무인기 관리 시스템

![Untitled](asset/Untitled.png)

![Untitled](asset/Untitled%201.png)

# Design and Implementation of a Blockchain-based Multi-UAV Mission Management System

基于区块链的多无人机任务管理方法的设计与实现

블록체인 기반 다중 무인기 관리 방법의 설계 및 구현

## Abstract


최근 몇 년 동안 무인 항공기(UAV) 산업은 항공 기술에 정보 기술이 완전히 침투하고 새로운 하드웨어가 개발됨에 따라 빠르게 성장했습니다. 새로운 하드웨어 및 부품의 개발로 인해 빠르게 성장하고 있습니다. 개방형 환경에서 운영되는 UAV는 데이터 저장 및 관리, 네트워크 통신 등 다양한 문제에 직면해 있습니다. 데이터 저장 및 관리, 네트워크 통신 등 다양한 문제에 직면해 있습니다. 이러한 문제에 대한 해결책으로 블록체인 기술이 주목받고 있습니다. 해시 함수와 암호화가 적용된 분산 원장을 사용하여 데이터를 안전하게 저장하고 관리하는 블록체인 기술이 주목받고 있습니다. 또한 블록체인 네트워크를 통해 드론의 보안성과 투명성을 향상시킬 수 있습니다. 본 논문에서는 기존 드론 임무 관리 시스템의 문제점에 대한 해결 방안을 연구하고 구현합니다. 논문에는 다음 세 가지가 포함됩니다. 

1. 드론에서 수집한 데이터를 안전하게 저장하기 위해 분산원장 데이터베이스를 구축합니다. 분산 분산원장은 블록체인 네트워크의 공유 데이터베이스로, 모든 네트워크 참여자가 데이터베이스에 접근하여 데이터를 추가할 수 있습니다. 데이터를 추가할 수 있지만, 암호화와 합의 알고리즘으로 인해 기존 데이터는 수정하거나 삭제할 수 없습니다.
2. 단일 지상국 기반 UAS 시스템의 문제점을 개선했습니다. 단일 지상국에서는 SPOF(단일 장애 지점)의 위험이 존재합니다. (단일 장애 지점) 위험. 즉, 하나의 중앙 노드에 장애가 발생하면 전체 시스템이 다운될 수 있습니다. 하나의 중앙 노드 장애로 인해 시스템이 다운될 수 있습니다. 이 논문에서는 확장성이 뛰어난 블록체인 네트워크와 함께 P2P 네트워크를 사용하여 다음과 같은 문제를 해결합니다. 이 문제를 해결하기 위해 
3. 드론의 실시간 성능을 보장하기 위해 CFT 기반의 빠른 합의 알고리즘을 사용합니다. 이는 더 적은 리소스를 사용하므로 실시간 드론 임무 관리가 가능합니다. 분산원장 관리, 프라이빗 블록체인, 사용자 인증 방식, 암호화 방식 등 다양한 기술을 접목하여 드론 임무 관리의 신뢰성을 높였습니다. 본 연구는 드론 임무 관리 시스템을 구축하여 드론 데이터 관리 및 네트워크 통신 문제를 효과적으로 해결할 수 있을 것으로 기대됩니다. 또한 본 논문에서는 미래 무인항공기 임무 관리 시스템을 제안합니다. 

또한 본 논문에서는 향후 연구 방향을 제안하고 이 기술이 적용될 수 있는 다양한 분야에 대해 논의합니다. 전반적으로 본 논문은 블록체인 기술을 활용하여 기존 무인항공기 관리 시스템 문제에 대한 해결책을 제시하고 있습니다. 이를 통해 무인항공기 산업 발전과 기술 혁신에 기여할 수 있을 것으로 기대합니다.

## 설계 방법 및 구현 방법


![Untitled](asset/Untitled%202.png)

시스템은 크게 Client, Block chain Network, FANET으로 구성되어 있습니다.

각 구성 요소는 각자의 역할을 수행하면 상호작용을 통해 시스템의 Flow를 진행합니다.

### Client

- Client 요소의 가장 큰 역할은 무인기 관리 플랫폼을 통해 무인기의 TASK(임무)를 관리하는 역할입니다.
- Django 기반의 MVT 아키텍처로 작성되었습니다. 템플릿은 부트 스트랩 기반의 웹 대시보드 형태로 구현되어 있고 Docker 를 사용한 컨테이너 과정이 포함되어 있습니다.

### Block Chain Network

- 블록체인 네트워크의 역할은 탈중앙화된 분산 시스템과 원장 구조를 사용하여 데이터를 안전하게 보관하고 단일 지상국의 문제점임 SPOF문제점을 해결하는 역할을 합니다.
- IBM 에서 개발한 Hyperledger Fabric 기반의 블록체인 네트워크를 사용합니다. Go 언어 기반의 SDK를 사용하기 위해 Go 언어 기반의 REST API와 Chain Code (core system)을 작성했습니다. 체인코드는 스마트컨트렉트 및 원장의 코드가 포함되어 있습니다.

### FANET

- FANET은 무인기의 독립적인 네트워크로 무인기간 통신을 위한 Ad-hoc 네트워크입니다. 본 연구에서는 Django, Celery, Redis를 사용한 비동기 처리 엔드포인트로 FANET의 역할을 대신합니다.

---

Design and Implementation of a Blockchain-based Multi-UAV Mission Management System 논문은 2023 beijing institute of technology에서 작성한 학위 논문입니다.
