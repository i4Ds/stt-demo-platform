import { Component, OnInit } from '@angular/core';
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-disclaimer-dialog',
  templateUrl: './disclaimer-dialog.component.html',
  styleUrls: ['./disclaimer-dialog.component.css']
})
export class DisclaimerDialogComponent implements OnInit {
  constructor(private dialogRef: MatDialogRef<DisclaimerDialogComponent>) {
    
  }

  ngOnInit(): void {
  }

  close() {
    this.dialogRef.close();
  }
}
