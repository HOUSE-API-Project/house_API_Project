#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

require 'snmp'
require 'fluent-logger'

necIXInternalTemperatureOID = "1.3.6.1.4.1.119.2.3.84.2.1.1.0"
Fluent::Logger::FluentLogger.open(nil, :host=>'133.242.144.202', :port=>19999)



while(true) 

    SNMP::Manager.open(:host=>'172.16.0.254', :community=>'public1', :version=>:SNMPv2c,) do |manager|
      response = manager.get([necIXInternalTemperatureOID])
      response.each_varbind{|v|
        puts v.value.to_s
      Fluent::Logger.post("shibuhouse.bf_kunugi", {"id"=>"wifi_temperture", "name"=>"#{v.value.to_s}"})
    }
    sleep(10)
    end
end

