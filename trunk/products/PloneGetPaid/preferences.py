"""

Annotation Property Storage and Site Configuration Settings

$Id$
"""

from getpaid.core.options import PersistentOptions

import interfaces

ConfigurationPreferences = PersistentOptions.wire("ConfigurationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementOptions )

#Profile
IdentificationPreferences = PersistentOptions.wire("IdentificationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementIdentificationOptions)
#Configure
ContentTypesPreferences = PersistentOptions.wire("ContentTypesPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementContentTypes )
   
ShippingOptionsPreferences = PersistentOptions.wire("ShippingOptionsPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementShippingOptions )

PaymentOptionsPreferences = PersistentOptions.wire("PaymentOptionsPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementPaymentOptions )
#Order Management
CustomerInformationPreferences = PersistentOptions.wire("CustomerInformationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementCustomerInformation )

OrderInformationPreferences = PersistentOptions.wire("OrderInformationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementOrderInformation)

PaymentProcessingPreferences = PersistentOptions.wire("PaymentProcessingPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementPaymentProcessing)

WeightUnitsPreferences = PersistentOptions.wire("WeightUnitsPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementWeightUnits)

SessionTimeoutPreferences = PersistentOptions.wire("SessionTimeoutPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementSessionTimeout)

SalesTaxPreferences = PersistentOptions.wire("SalesTaxPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementSalesTaxOptions)
#Currency
CurrencyPreferences = PersistentOptions.wire("CurrencyPreferences",
                                             "getpaid.configuration",
                                             interfaces.IGetPaidManagementCurrencyOptions )    
#Emails 
EmailPreferences = PersistentOptions.wire("EmailPreferences",
                                          "getpaid.configuration",
                                          interfaces.IGetPaidManagementEmailOptions )    

CustomerNotificationPreferences = PersistentOptions.wire("CustomerNotificationPreferences",
                                                         "getpaid.configuration",
                                                         interfaces.IGetPaidManagementCustomerNotificationOptions )                                                     

MerchantNotificationPreferences = PersistentOptions.wire("MerchantNotificationPreferences",
                                                         "getpaid.configuration",
                                                         interfaces.IGetPaidManagementMerchantNotificationOptions )   
#Customize Header/Footer 
HeaderFooterPreferences = PersistentOptions.wire("HeaderFooterPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementHeaderFooterOptions )    
  