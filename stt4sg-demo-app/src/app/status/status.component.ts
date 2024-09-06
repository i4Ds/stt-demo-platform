import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router'
import {ToastrService} from "ngx-toastr";
import {APIService, Status} from "../Services/API/api.service";
import {Subscription, timer} from 'rxjs';
import { map } from 'rxjs/operators';


@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
    id: string | null = null;
    status: Status | null = null;
    timerSubscription: Subscription | null = null; 

    constructor(private router: Router,
                private toastr: ToastrService,
                private apiService: APIService,
                private route: ActivatedRoute) {

    }

    ngOnInit(): void {
        this.route.paramMap.subscribe((params: ParamMap) => {
            this.id = params.get('id')
        })

        this.timerSubscription = timer(0, 10000).pipe( 
            map(() => { 
              this.update_status();
            }) 
        ).subscribe(); 
    }

    update_status() {
        if (this.id) {
            this.apiService.longStatus(this.id).subscribe(
                x => {
                    this.status = x
                }, error => {
                    
                }
            );
        }
    }

    ngOnDestroy(): void { 
        this.timerSubscription?.unsubscribe(); 
    } 
}
