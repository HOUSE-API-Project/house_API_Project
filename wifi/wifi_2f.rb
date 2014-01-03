require 'rest-client'
require 'snmp'
require 'json'

wifi_twof_host = '172.16.0.253'
twof_wifi_clients = '1.3.6.1.4.1.9.9.273.1.1.2.1.1'
counter = 0
twof_wifi_clients_low = 0
twof_wifi_clients_high = 0
community_pass = "COMMUNITY_PASSWORD"
basicID = "BASICID"
basicPASS = "BASICPASS"
post_url = 'http://'<< basicID << ':' << basicPASS << '@house-api-project.org/post'

SNMP::Manager.open(:host=>wifi_twof_host, :community=>community_pass, :version=>:SNMPv2c,) do |manager|
      manager.walk(twof_wifi_clients) do |row|
        if counter == 0
          twof_wifi_clients_low = row.value
        elsif counter == 1
          twof_wifi_clients_high = row.value
        end
        counter += 1
      end

      twof_wifi_all_clients = twof_wifi_clients_low.to_i + twof_wifi_clients_high.to_i
  json = {"all_clients" => "#{twof_wifi_all_clients}", "clients_low_speed" => "#{twof_wifi_clients_low}", "clients_high_speed" => "#{twof_wifi_clients_high}"}
      tag = "shibuhouse.wifi.2f.clients"
  response = RestClient.post(post_url , {:tag => tag, :data => json},{:content_type => :json, :accept => :json})

      #lowspeed send
  json = {"clients_low_speed" => "#{twof_wifi_clients_low}"}
      tag = "shibuhouse.wifi.2f.clients_low_speed"
  response = RestClient.post(post_url , {:tag => tag, :data => json},{:content_type => :json, :accept => :json})

      #highspeed send
  json = {"clients_high_speed" => "#{twof_wifi_clients_high}"}
      tag = "shibuhouse.wifi.2f.clients_high_speed"
  response = RestClient.post(post_url , {:tag => tag, :data => json},{:content_type => :json, :accept => :json})
end
