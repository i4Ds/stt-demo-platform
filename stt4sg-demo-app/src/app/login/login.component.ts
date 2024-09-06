import { Component, OnInit } from '@angular/core';
import { CookieService } from "ngx-cookie-service";
import { AuthService } from "../Services/auth.service";
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  password: string = "";

  constructor(private cookieService: CookieService,
              private auth: AuthService,
              private router: Router,
              private toastr: ToastrService) {
    this.password = cookieService.get("Password");
    this.login(false);
  }

  ngOnInit(): void {
  }

  login(showError = true) {
    this.auth.login(this.password).then((valid) => {
      if(valid){
        this.cookieService.set("Password", this.password);
        this.router.navigateByUrl('/record')
      } else {
        this.password = "";
        if(showError){
          this.toastr.error("Wrong password!")
        }
      }
    });
  }
}
