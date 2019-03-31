## Example Project for django_private_chat

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Navigate to the `example` directory
2. Create virtualenv with the desired python >= 3.4:

        virtualenv venv -p python3
        source venv/bin/activate
	(For Windows User)
	venv\Scripts\activate
        
3. Install the requirements for the package:
		
		pip install -r requirements.txt
		
4. Apply migrations:
		
		python manage.py migrate
		python manage.py loaddata fixtures/init_data.json
		
5. Run the server

		python manage.py runserver
		
6. Run chat server in separate terminal
        
        python manage.py run_chat_server
7. Access from the browser at `http://127.0.0.1:8000`

There are two example users: user_1 and user_2. They have the same password: pa$$word
