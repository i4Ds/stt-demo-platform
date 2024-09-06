import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  columns: number = 1;
  constructor(private router: Router,
              private toastr: ToastrService,
              ) {

  }

  ngOnInit(): void {
    this.columns = (window.innerWidth <= 400) ? 1 : (window.innerWidth <= 800) ? 2 : 3 ;
  }
  handleResize(event: UIEvent) {
    this.columns = (window.innerWidth <= 400) ? 1 : (window.innerWidth <= 800) ? 2 : 3 ;
  }
}
