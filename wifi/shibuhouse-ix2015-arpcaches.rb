#!/usr/bin/env ruby 
# -*- coding: utf-8 -*-

require 'snmp'
arpcachetablesOID = "1.3.6.1.2.1.3.1.1.2"


clients=0

SNMP::Manager.open(:host=>'172.16.0.254', :community=>'public1', :version=>:SNMPv2c,) do |manager|
  manager.walk(arpcachetablesOID) do |row|
    clients += 1
    puts "#{clients}: #{row}"
  end
end

printf("clients: %d\n", clients)
