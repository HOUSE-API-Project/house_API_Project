require 'rest-client'

require 'snmp'
require 'json'

necIXInternalTemperatureOID = "1.3.6.1.4.1.119.2.3.84.2.1.1.0"
arpcachetablesOID = "1.3.6.1.2.1.3.1.1.2"
cachetablesOID = "1.3.6.1.2.1.3.1.1.2"
id = "shibuhouse"
community_pass = "COMMUNITY_PASSWORD"
#while(true)
  clients = 0
  temperature = 0
    SNMP::Manager.open(:host=>'172.16.0.254', :community=>community_pass, :version=>:SNMPv2c,) do |manager|

      #wifi connecting clients
      manager.walk(arpcachetablesOID) do |row|
        clients += 1
      end
        #puts clients
    json = {"clients" => "#{clients}"}
    tag = "shibuhouse.wifi.clients"
    response = RestClient.post('http://houseapi:kogaidan@133.242.144.202/post', {:tag => tag, :data => json},{:content_type => :json, :accept => :json})

      #wifi temperature
    response = manager.get([necIXInternalTemperatureOID])
    response.each_varbind{|v|
        temperature = v.value.to_s
        #puts v.value.to_s

      json = {"temperature" => "#{v.value.to_s}"}
      tag = "shibuhouse.wifi.temperature"
      response = RestClient.post('http://houseapi:kogaidan@133.242.144.202/post', {:tag => tag, :data => json},{:content_type => :json, :accept => :json})
    }

    json = {"clients" => "#{clients}", "temperature" => "#{temperature}"}
    tag = "shibuhouse.wifi"
    response = RestClient.post('http://houseapi:kogaidan@133.242.144.202/post', {:tag => tag, :data => json},{:content_type => :json, :accept => :json})
    #sleep(10)
    end
#end