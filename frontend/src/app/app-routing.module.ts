import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StartComponent } from './components/start/start.component';
import { SigninComponent } from './components/auth/signin/signin.component';
import { SignupComponent } from './components/auth/signup/signup.component';
import { MentorComponent } from './components/dashboard-mentor/mentor/mentor.component';
import { MenteeComponent } from './components/dashboard-mentee/mentee/mentee.component';
import { AboutComponent } from './components/about/about.component';

const routes: Routes = [
  { path: 'start', component: StartComponent },
  { path: 'about', component: AboutComponent },
  { path: '', pathMatch: 'full', component: StartComponent },
  { path: 'auth/sign-in', component: SigninComponent },
  { path: 'auth/sign-up', component: SignupComponent },
  { path: 'dashboard/mentor', component: MentorComponent },
  { path: 'dashboard/mentee', component: MenteeComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
