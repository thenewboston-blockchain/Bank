## Project Setup

Install required packages:
```
sudo pip3 install -r requirements/local.txt
```

When adding a package, add to `requirements/base.in` and then :

```
bash scripts/compile_requirements.sh
```

Initialize database:
```
python3 manage.py migrate
```
