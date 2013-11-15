require 'rest-client'
require 'snmp'
require 'json'

onef_wifi = '1.3.6.1.4.1.672.43.3.4.2.1.10.4.0'
onef_wifi_highspeed = '1.3.6.1.4.1.672.43.3.3.1.10.4.0'
host_onef = '172.16.0.251'
id = "shibuhouse"
clients_low = 0
clients_high = 0
community_pass = "COMMUNITY_PASSWORD"
basicID = "BASICID"
basicPASS = "BASICPASS"
post_url = 'http://'<< basicID << ':' << basicPASS << '@133.242.144.202/post'

SNMP::Manager.open(:host=>host_onef, :community=>community_pass, :version=>:SNMPv1,) do |manager|
   response = manager.get([onef_wifi])
  response.each_varbind { |v|
        clients_low = v.value.to_s
  }
         #puts clients
  json = {"clients_low" => "#{clients_low}", "locational_time" => "#{locational_time}"}
    tag = "shibuhouse.wifi.1f.clients_low_speed"
  response = RestClient.post(post_url, {:tag => tag, :data => json},{:content_type => :json, :accept => :json})

   response = manager.get([onef_wifi_highspeed])
  response.each_varbind { |v|
        clients_high = v.value.to_s
  }
    json = {"clients_high" => "#{clients_high}","locational_time" => "#{locational_time}"}
    tag = "shibuhouse.wifi.1f.clients_high_speed"
  response = RestClient.post(post_url, {:tag => tag, :data => json},{:content_type => :json, :accept => :json})


  clients_all = clients_low.to_i + clients_high.to_i
      json = {"all_clients" => "#{clients_all}", "clients_high_speed" => "#{clients_high}", "clients_low_speed" => "#{clients_low}", "locational_time" => "#{locational_time}"}
    tag = "shibuhouse.wifi.1f.clients"
  response = RestClient.post(post_url, {:tag => tag, :data => json},{:content_type => :json, :accept => :json})
end