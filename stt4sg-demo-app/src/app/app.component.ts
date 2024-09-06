import {Component} from '@angular/core';
import {MatDialog, MatDialogConfig} from "@angular/material/dialog";
import { DisclaimerDialogComponent } from './disclaimer-dialog/disclaimer-dialog.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'stt4sg-demo-app';

  constructor(private dialog: MatDialog) {}

  openDisclaimerDialog() {

        const dialogConfig = new MatDialogConfig();

        dialogConfig.disableClose = true;
        dialogConfig.autoFocus = true;

        this.dialog.open(DisclaimerDialogComponent, dialogConfig);
  }
}
