import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from "./login/login.component";
import { RecordingComponent} from "./recording/recording.component";
import { AppComponent } from "./app.component";

const routes: Routes = [
  //{ path: "login", component: LoginComponent },
  {
    path: '',
    component: AppComponent,
    children: [
      { path: "", redirectTo: '/record', pathMatch: "full"},
      { path: "record", component: RecordingComponent },
      { path: "**", redirectTo: '/record' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
