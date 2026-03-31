from app import create_app
from app.db import db
from app.models import User

app = create_app()
app.app_context().push()

# Check if admin already exists
admin = User.query.filter_by(username="admin").first()
if not admin:
    admin = User(username="admin", display_name="Administrator")
    admin.set_password("admin")  
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")
else:
    print("Admin already exists!")
