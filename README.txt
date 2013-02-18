#   Copyright 2012 UFRGS
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

                 					ProViNet


What is ProViNet?
'''''''''''''''''''''''''''''''''''''''''''''''''''''

ProViNet is an open platform for Programmable Virtual Networking management. 

The current release of ProViNet supports the following features:

    * Programmable Virtual Network (PVN) infrastructure provisioning
    * Creating network applications to control PVNs
    * Managing clusters of controllers
    * Creation and deployment of network applications
    * Sharing network applications
    * Team development of network applications
    * Multiples controller vendors support (since it follows REST architecture)
    * Registering controller services, which may vary among different vendors
    * End Users Access and Authentication Control

Configurations required
'''''''''''''''''''''''''''''''''''''''''''''''''''''
    
     In order to have ProViNet deployed, folow the following procedure:
    
    * Configure a Scalable Control Pool (virtualization server pool, such as XenServer)
      in the admin page (Ex.:localhost:8080/admin)
    * Deploy FloodLight controller in a Virtual Machine in the Scalable Control Pool
      and name it "controller"
    * Configure in the ProViNet admin page the controller access informations such as
      url, username, password, port... 


What's here?
------------

The main components of this distribution are:

    * ProViNet Core
    * 

What other documentation is available?
--------------------------------------

Further informations will come

Contact 
-------

http://www.futureinternet.br/provinet
