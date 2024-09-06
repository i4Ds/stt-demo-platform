import {APP_INITIALIZER, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from "./app-routing.module";
import { FormsModule } from "@angular/forms";

import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { ToastrModule } from "ngx-toastr";
import {HttpClientModule} from "@angular/common/http";

import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { CardComponent } from './card/card.component';
import { LongComponent } from './long/long.component';
import { StatusComponent } from './status/status.component';
import { DisclaimerDialogComponent } from './disclaimer-dialog/disclaimer-dialog.component'

import { NgxDropzoneModule } from 'ngx-dropzone';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatDialogModule} from "@angular/material/dialog";
import {MatGridListModule} from "@angular/material/grid-list";
import {MatListModule} from "@angular/material/list";

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    CardComponent,
    LongComponent,
    StatusComponent,
    DisclaimerDialogComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot({
      timeOut: 7000,
      progressBar: true,
      positionClass: 'toast-bottom-left'
    }),
    HttpClientModule,
    NgxDropzoneModule,
    MatProgressBarModule,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatGridListModule,
    MatListModule
  ],
  exports: [HomeComponent, CardComponent, LongComponent, StatusComponent],
  providers: [AppComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
