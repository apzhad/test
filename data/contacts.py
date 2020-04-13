from model.contact import Contact


test_data = [
    Contact(first_name="first_name ", middle_name="middle_name", last_name="last_name", nickname="nickname",
            title="title", company="company", address="address", home_phone="homephone",
            mobile_phone="mobilephone", work_phone="workphone", fax="fax", primary_email="email",
            secondary_email="email2", third_email="email3", homepage="homepage", birth_day="1",
            birth_month="May", birth_year="1950", anniversary_day="15", anniversary_month="June",
            anniversary_year="2000", secondary_address="address secondary",
            secondary_home_phone="home secondary", notes="notes", photo_path="cat.jpg"),
    Contact(first_name="test"),
    Contact(first_name="fname ", last_name="lname", address="adr\nto\nsource", home_phone="78204")
    ]
