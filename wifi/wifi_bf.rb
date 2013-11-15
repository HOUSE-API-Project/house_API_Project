require 'snmp'
require 'json'

wifi_twof_host = '172.16.0.252'
twof_wifi_clients = '1.3.6.1.4.1.9.9.273.1.1.2.1.1'
counter = 0
bf_wifi_clients = 0
community_pass = "COMMUNITY_PASSWORD"

SNMP::Manager.open(:host=>wifi_twof_host, :community=>community_pass, :version=>:SNMPv2c,) do |manager|
      manager.walk(twof_wifi_clients) do |row|
        bf_wifi_clients = row.value.to_s
      end

    json = {"all_clients" => "#{bf_wifi_clients}"}
    tag = "shibuhouse.wifi.bf.clients"
    response = RestClient.post('http://houseapi:kogaidan@133.242.144.202/post', {:tag => tag, :data => json},{:content_type => :json, :accept => :json})
end