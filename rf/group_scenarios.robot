*** Settings ***
Library  rf.Addressbook
Library  Collections
Suite Setup  Init fixture
Suite Teardown  Finish Fixture


*** Test Cases ***
Add new group
    ${old_list}=  Get Group list
    ${group}=  New Group  name1  header1  footer1
    Create Group  ${group}
    ${new_list}=  Get Group list
    Append To List  ${old_list}  ${group}
    Group Lists Should Be Equal  ${old_list}  ${new_list}

Delete group
    ${old_list}=  Get Group list
    ${len}=  Get Length  ${old_list}
    ${index}=  Evaluate  random.randrange(${len})  random
    ${group}=  Get From List  ${old_list}  ${index}
    Delete Group  ${group}
    ${new_list}=  Get Group list
    Remove Values From List  ${old_list}  ${group}
    Group Lists Should Be Equal  ${old_list}  ${new_list}
