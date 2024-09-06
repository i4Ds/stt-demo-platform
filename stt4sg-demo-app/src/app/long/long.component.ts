import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";
import {APIService, Status} from "../Services/API/api.service";
import { Subscription } from 'rxjs/internal/Subscription';
import { HttpEventType } from '@angular/common/http';
import { finalize } from 'rxjs/operators';
import {AppComponent} from '../app.component';

@Component({
  selector: 'app-long',
  templateUrl: './long.component.html',
  styleUrls: ['./long.component.css']
})
export class LongComponent implements OnInit {
  fileName = '';
  uploadProgress:number = 0;
  uploadSub: Subscription | null = null;
  id: string | null = null;

  constructor(private router: Router,
              private toastr: ToastrService,
              private apiService: APIService,
              public myapp: AppComponent) {
    
  }

  ngOnInit(): void {
  }  

	onFileSelected(e: File[]) {
    const file:File = e[0]

    if (file) {
        this.fileName = file.name;
        const formData = new FormData();
        formData.append("file", file);

        const upload$ = this.apiService.upload(file, this.fileName).pipe(finalize(() => this.reset()));
      
        this.uploadSub = upload$.subscribe((event: any) => {
          if (event.type == HttpEventType.UploadProgress) {
            this.uploadProgress = Math.round(100 * (event.loaded / event.total));
          }
          else {
            if (event.body?.id) {
              this.id = event.body?.id
            } 
          }
        })
    }
  }

  reset() {
    if (this.id){
      this.uploadProgress = 0;
      this.uploadSub = null;
      this.router.navigate(['/status', this.id])
    }
  }

  opendialog() {
    this.myapp.openDisclaimerDialog();
  }
}
