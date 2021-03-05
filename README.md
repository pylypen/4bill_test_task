# 4bill Test Task
##
List of Python libs in `requirements.txt`.

Copy `/app/.env.example` and rename to `/app/.env`
##
## Docker's command helpers
- Build\Rebuild of containers `docker-compose up --build` or `docker-compose up -d --build` add ahead `sudo` for ubuntu/linux
- Start of containers `docker-compose up` or `docker-compose up -d` add ahead `sudo` for ubuntu/linux
- Stop of containers `docker-compose down` add ahead `sudo` for ubuntu/linux
- Checking logs `docker-compose logs --tal 25`
- Navigate to http://localhost:5000/request/100
###
## Command for Run tests
- Open a new terminal tab/window run `docker-compose exec app bash` add ahead `sudo` for ubuntu/linux
- And run `pytest`
##