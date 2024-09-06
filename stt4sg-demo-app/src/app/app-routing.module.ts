import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from "./home/home.component"
import { LongComponent } from "./long/long.component";
import { StatusComponent } from "./status/status.component"
import { AppComponent } from "./app.component";
import {CardComponent} from "./card/card.component";

const routes: Routes = [
  {
    path: '',
    component: AppComponent,
    children: [
      { path: "", redirectTo: '/home', pathMatch: "full"},
      { path: "home", component: HomeComponent },
      { path: "record", component: CardComponent },
      { path: "long", component: LongComponent},
      { path: "status/:id", component: StatusComponent},
      { path: "**", redirectTo: '/home' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
