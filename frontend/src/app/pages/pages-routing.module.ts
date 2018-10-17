import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import {NbBadgeModule} from '@nebular/theme';
// import { NotFoundComponent } from './miscellaneous/not-found/not-found.component';

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [ {
    path: 'dashboard',
    component: DashboardComponent,
  },  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  }, {
    path: '**',
    // component: NotFoundComponent,
    redirectTo: 'dashboard',
  }],
}];

@NgModule({
  imports: [RouterModule.forChild(routes),
      NbBadgeModule],
  exports: [RouterModule],
})
export class PagesRoutingModule {
}
