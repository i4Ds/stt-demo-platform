import { Component, OnInit } from '@angular/core';
import { CookieService } from "ngx-cookie-service";
import { AuthService } from "../Services/auth.service";
import { Router } from "@angular/router";
import {invokeSaveAsDialog, MediaStreamRecorder, RecordRTCPromisesHandler, StereoAudioRecorder} from "recordrtc";
import {APIService} from "../Services/API/api.service";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-recording',
  templateUrl: './recording.component.html',
  styleUrls: ['./recording.component.css']
})
export class RecordingComponent implements OnInit {

  recorder: RecordRTCPromisesHandler|null = null;

  microphoneok:boolean = false;
  startedRecording:boolean = false;
  stoppedRecording:boolean = false;
  hasRecording:boolean = false;
  timestampStart = 0;
  timestampEnd = 0;
  timeRecorded = 0;
  timeout_id = -1;

  result:string = ""

  constructor(private cookieService: CookieService,
              private auth: AuthService,
              private router: Router,
              private apiService: APIService,
              private toastr: ToastrService) {
    //this.checkLogin();
    this.initRecorder();
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
    new Promise<RecordRTCPromisesHandler>(() => {
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
    this.timeout_id = setTimeout(() => this.stopRecording(), 15000)
    setTimeout(() => this.getRecordingTime(), 10)
  }

  stopRecording() {
    if(this.startedRecording) {
      clearTimeout(this.timeout_id)
      this.recorder?.stopRecording();
      this.stoppedRecording = true;
      this.hasRecording = true;
      this.startedRecording = false;
    }
  }

  async save() {
    let blob = this.recorder?.getBlob();
    if (blob) {
      invokeSaveAsDialog(await blob);
    }
    //let src = URL.createObjectURL(blob);
  }

  async send() {
    let blob = await this.recorder?.getBlob();
    if(blob){
      let data = new FormData();
      data.append('file', blob, "audio.wav");
      this.apiService.getTranslation(data).subscribe(
        x => {
          this.result = x
        }, error => {
          this.toastr.error("Ein Fehler ist aufgetreten!")
          console.log("error")
          console.log(error);
        }
      );
    }
  }

  getRecordingTime() {
      const current = new Date();
      this.timestampEnd = current.getTime();
      this.timeRecorded = (this.timestampEnd - this.timestampStart) / 1000;

      if(!this.hasRecording){
        setTimeout(() => this.getRecordingTime(), 10)
      }
  }
}
