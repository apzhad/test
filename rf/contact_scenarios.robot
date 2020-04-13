*** Settings ***
Library  rf.Addressbook
Library  Collections
Suite Setup  Init fixture
Suite Teardown  Finish Fixture

*** Test Cases ***
Add new contact
    ${old_list}=  Get Contact List
    ${contact}=  New Contact  first_name1  last_name1  address1  12345
    Create Contact  ${contact}
    ${new_list}=  Get Contact List
    Append To List  ${old_list}  ${contact}
    Contact Lists Should Be Equal  ${old_list}  ${new_list}

Modify contact
    Check Contact Exist
    ${old_list}=  Get Contact List
    ${len}=  Get Length  ${old_list}
    ${modify_data}=  New Contact  fffirst  modify_ln1  some_addr1  29-789-45
    ${index}=  Evaluate  random.randrange(${len})  random
    ${contact}=  Get From List  ${old_list}  ${index}
    Modify Contact  ${contact}  ${modify_data}
    ${new_list}=  Get Contact list
    Set List Value  ${old_list}  ${index}  ${modify_data}
    Contact Lists Should Be Equal  ${old_list}  ${new_list}

Modify contact from detail
    Check Contact Exist
    ${old_list}=  Get Contact List
    ${len}=  Get Length  ${old_list}
    ${modify_data}=  New Contact  fffirst  modify_ln1  some_addr1  29-789-45
    ${index}=  Evaluate  random.randrange(${len})  random
    ${contact}=  Get From List  ${old_list}  ${index}
    Modify Contact From Detail  ${contact}  ${modify_data}
    ${new_list}=  Get Contact list
    Set List Value  ${old_list}  ${index}  ${modify_data}
    Contact Lists Should Be Equal  ${old_list}  ${new_list}

Delete contact
    Check Contact Exist
    ${old_list}=  Get Contact List
    ${len}=  Get Length  ${old_list}
    ${index}=  Evaluate  random.randrange(${len})  random
    ${contact}=  Get From List  ${old_list}  ${index}
    Delete Contact  ${contact}
    ${new_list}=  Get Contact list
    Remove Values From List  ${old_list}  ${contact}
    Contact Lists Should Be Equal  ${old_list}  ${new_list}

Cancel delete contact
    Check Contact Exist
    ${old_list}=  Get Contact List
    ${len}=  Get Length  ${old_list}
    ${index}=  Evaluate  random.randrange(${len})  random
    ${contact}=  Get From List  ${old_list}  ${index}
    Cancel Delete Contact  ${contact}
    ${new_list}=  Get Contact list
    Contact Lists Should Be Equal  ${old_list}  ${new_list}

Delete all contacts
    Check Contact Exist
    Delete All Contacts
    ${new_list}=  Get Contact list
    Contact List Should Be Empty  ${new_list}