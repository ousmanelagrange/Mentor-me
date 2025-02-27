import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { RequestService } from 'src/app/services/request.service';
import { RouterService } from 'src/app/services/router.service';

@Component({
  selector: 'app-session-mentee',
  templateUrl: './session-mentee.component.html',
  styleUrls: ['./session-mentee.component.scss']
})
export class SessionMenteeComponent implements OnInit {
  active = 1
  loading = false
  user_id = null
  type: Array<string> = ["Atelier", "Session de questions-réponses", "Session de feedback", "Session de mentorat", "Session de planification de carrière", "ession de révision de CV/lettre de motivation", "Session de préparation à l'entretien", "Session de groupe "]
  disponibilite: Array<any> = []
  users: Array<any> = []
  sessions: Array<any> = []
  formForm!: FormGroup;

  constructor(public requestService: RequestService, private formBuilder: FormBuilder, private routerService: RouterService) { }
  ngOnInit(): void {
    this.chargeSession();
  }


  changeActive(active: number) {
    this.active = active
  }




  chargeSession() {
    this.changeActive(1)
    this.loading = true
    const userString = localStorage.getItem('user');
    if (userString !== null) {
      const user = JSON.parse(userString);
      if (user.is_mentor) {
        this.routerService.routeRoute('/auth/sign-in');
      } else {
        let data = {
          "action": 5,
          "mentee": user.id
        };
        this.requestService.post("https://mentor-me-7viu.onrender.com/api/sessions/", data).then(
          (res: any) => {
            console.log(res)
            this.sessions = res
            this.loading = false;
          }
        )
      }
    } else {
      this.routerService.routeRoute('/auth/sign-in');
    }
  }

}
