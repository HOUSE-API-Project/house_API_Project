  #!/usr/bin/env ruby
# -*- coding: utf-8 -*-

require 'snmp'
require 'fluent-logger'
require 'json'

necIXInternalTemperatureOID = "1.3.6.1.4.1.9.9.273.1.1.2.1.1"
arpcachetablesOID = "1.3.6.1.2.1.3.1.1.2"
cachetablesOID = "1.3.6.1.2.1.3.1.1.2"
Fluent::Logger::FluentLogger.open(nil, :host=>'133.242.144.202', :port=>19999)


while(true) 
  clients = 0
  temperature = 0
    SNMP::Manager.open(:host=>'172.16.0.253', :community=>'public1', :version=>:SNMPv2c,) do |manager|

      #wifi connecting clients
      manager.walk(arpcachetablesOID) do |row|
        clients += 1
      end
        puts clients
    Fluent::Logger.post("shibuhouse.wificlients", {"id"=>"kokoni_nani", "clients"=>"#{clients}"})

      #wifi temperture
    response = manager.get([necIXInternalTemperatureOID])
    response.each_varbind{|v|
        temperature = v.value.to_s
        puts v.value.to_s
      Fluent::Logger.post("shibuhouse.wifitemperature", {"id"=>"kokoni_nani", "temperature"=>"#{v.value.to_s}"})
    }

    Fluent::Logger.post("shibuhouse.wifi", {"id"=>"kokoni_nani", "temperature"=>"#{temperature}", "clients" => "#{clients}"})
    sleep(10)
    end
end
