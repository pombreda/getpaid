"""

Annotation Property Storage and Site Configuration Settings

$Id$
"""

from getpaid.core.options import PersistentOptions

import interfaces

ConfigurationPreferences = PersistentOptions.wire("ConfigurationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementOptions )
    
IdentificationPreferences = PersistentOptions.wire("IdentificationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementIdentificationOptions )    
    
CurrencyPreferences = PersistentOptions.wire("CurrencyPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementCurrencyOptions )    
 
MaintenancePreferences = PersistentOptions.wire("MaintenancePreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementMaintenanceOptions )    
 
EmailPreferences = PersistentOptions.wire("EmailPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementEmailOptions )    
 
HeaderFooterPreferences = PersistentOptions.wire("HeaderFooterPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementHeaderFooterOptions )    
  