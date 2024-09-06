import { Component, OnInit } from '@angular/core';
import {invokeSaveAsDialog, RecordRTCPromisesHandler, StereoAudioRecorder} from "recordrtc";
import {CookieService} from "ngx-cookie-service";
import {AuthService} from "../Services/auth.service";
import {Router} from "@angular/router";
import {APIService, Transcription} from "../Services/API/api.service";
import {ToastrService} from "ngx-toastr";
import {MatomoService} from "../Services/matomo.service";
import {AppComponent} from '../app.component';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {

  toggleProperty = false;

  toggle() {
    this.toggleProperty = !this.toggleProperty;
  }
  recorder: RecordRTCPromisesHandler|null = null;

  microphoneok:boolean = false;
  startedRecording:boolean = false;
  stoppedRecording:boolean = false;
  hasRecording:boolean = false;
  timestampStart = 0;
  timestampEnd = 0;
  timeRecorded = 0;
  timeout_id = -1;
  rating = 0;
  ratingHover = 0;
  result: Transcription | null = null;

  constructor(private cookieService: CookieService,
              private auth: AuthService,
              private router: Router,
              private apiService: APIService,
              private toastr: ToastrService,
              private matomo: MatomoService,
              public myapp: AppComponent) {
    //this.checkLogin();
    this.initRecorder();
    this.matomo.getVisitorId().then(x => console.log('visitorId', x))
  }

  ngOnInit(): void {
  }
  /*checkLogin() {
    this.auth.login(this.cookieService.get("Password")).then((valid) => {
      if(!valid){
        this.router.navigateByUrl('/login')
      }
    });
  }*/

  initRecorder() {
    navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
        this.recorder =  new RecordRTCPromisesHandler(stream, {
          type: 'audio',
          mimeType: 'audio/wav',
          recorderType: StereoAudioRecorder,
        });
        this.microphoneok = true;
      },
      catchError => {
        this.microphoneok = false;
      });
  }

  async startRecording() {
    await this.recorder?.reset();
    this.timestampStart = 0;
    this.timestampEnd = 0;
    this.hasRecording = false;
    this.startedRecording = true;

    const current = new Date();
    this.timestampStart = current.getTime();

    this.recorder?.startRecording();
    this.timeout_id = window.setTimeout(() => this.send(), 15000)
    setTimeout(() => this.getRecordingTime(), 10)
  }

  async send() {
    if(this.startedRecording) {
      clearTimeout(this.timeout_id)
      this.stoppedRecording = true
      this.hasRecording = true
      this.startedRecording = false
      const blob = await this.recorder?.stopRecording().then(() => this.recorder?.getBlob())
      if (blob) {
        this.apiService.getTranslation(blob).subscribe(
          x => {
            this.result = x
            this.matomo.trackEvent("stt", "transcribe", x.id)
            this.toggle()
          }, error => {
            this.toastr.error("Ein Fehler ist aufgetreten!")
            this.resetRecording()
          }
        );
      } else {
        this.toastr.error("Ein Fehler ist aufgetreten!")
        this.resetRecording()
      }
    }
  }

  async sendRating() {
    const id = this.result?.id
    if (id) {
      await this.apiService.submitRating(id, {rating: this.rating}).subscribe(
        x => {
          this.matomo.trackEvent("stt", "rate", x.id, this.rating)
          this.toastr.success("Rating wurde abgesendet!")
        }, error => {
          this.toastr.error("Ein Fehler ist aufgetreten!")
        }
      );
    }
  }

  resetRecording() {
    this.toggleProperty = false;
    this.startedRecording = false;
    this.stoppedRecording = false;
    this.hasRecording = false;
    this.rating = 0;
    this.ratingHover = 0;
    this.result = null;
  }


  getRecordingTime() {
    const current = new Date();
    this.timestampEnd = current.getTime();
    this.timeRecorded = (this.timestampEnd - this.timestampStart) / 1000;

    if(!this.hasRecording){
      setTimeout(() => this.getRecordingTime(), 10)
    }
  }

  opendialog() {
    this.myapp.openDisclaimerDialog();
  }
}
