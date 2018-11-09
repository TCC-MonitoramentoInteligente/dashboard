## MIA Dashboard Frontend

### Requirements
- Nodejs (https://nodejs.org/en/download/package-manager/)
- Angular (```sudo npm install -g @angular/cli```)

### Setup
- Set the variable `SERVER_URL` in `frontend/src/app/@core/data/event-list.service.ts`
- Set the url in `frontend/src/app/pages/dashboard/security-cameras/security-cameras.component.html`

### Run
Inside frontend directory.
```
npm install
ng serve --host <IP_HOST> --port <PORT>
```
### Dashboard Page
```
http://<IP_HOST>:<PORT>/
```

#### References
Template based on https://github.com/akveo/ngx-admin 
