Scenario Outline: Add new contact
  Given a contact list
  Given a contact with <first_name>, <last_name>, <address> and <home_phone>
  When I add the contact to the list
  Then the new contact list is equal to the old list with the added contact

  Examples:
  | first_name  | last_name  | address  | home_phone |
  | first_name1 | last_name1 | address1 | 12345      |
  | first_name2 | last_name2 | address2 | 78960      |

Scenario Outline: Modify contact
  Given a non-empty contact list
  Given a random contact from the list
  Given a <first_name>, <last_name>, <address> and <home_phone> for modify
  When I modify the contact from the list
  Then the new contact list is equal to the old list with modified contact

  Examples:
  | first_name | last_name  | address    | home_phone |
  | modify_fn1 | modify_ln1 | some_addr1 | 29-789-45  |
  | modify_fn2 | modify_ln2 | some_addr2 | 8347894    |

Scenario Outline: Modify contact from detail
  Given a non-empty contact list
  Given a random contact from the list
  Given a <first_name>, <last_name>, <address> and <home_phone> for modify
  When I open details and modify the contact from the list
  Then the new contact list is equal to the old list with modified contact

  Examples:
  | first_name | last_name  | address    | home_phone |
  | modify_fn1 | modify_ln1 | some_addr1 | 29-789-45  |
  | modify_fn2 | modify_ln2 | some_addr2 | 8347894    |

Scenario: Delete contact
  Given a non-empty contact list
  Given a random contact from the list
  When I delete the contact from the list
  Then the new contact list is equal to the old list without the deleted contact

Scenario: Cancel delete contact
  Given a non-empty contact list
  Given a random contact from the list
  When I delete the contact from the list and cancel deletion
  Then the new contact list is equal to the old list without changes

Scenario: Delete all contacts
  Given a non-empty contact list
  When I click on "Select all" and then delete contacts
  Then the new contact list is empty