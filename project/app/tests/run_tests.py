import subprocess

# subprocess.run(["pytest", "app/tests/test_delete.py", "-vv"], check=True)
# subprocess.run(["pytest", "app/tests/test_get_user.py", "-vv"], check=True)
# subprocess.run(["pytest", "app/tests/test_get_users.py", "-vv"], check=True)
# subprocess.run(["pytest", "app/tests/test_login.py", "-vv"], check=True)
subprocess.run(["pytest", "app/tests/test_post.py", "-vv"], check=True)
subprocess.run(["pytest", "app/tests/test_put.py", "-vv"], check=True)
subprocess.run(["pytest", "app/tests/test_signup.py", "-vv"], check=True)