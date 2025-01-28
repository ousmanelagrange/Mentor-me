import { Component } from '@angular/core';
import { FormGroup, FormBuilder, FormArray, Validators } from '@angular/forms';
import { RequestService } from 'src/app/services/request.service';
import { RouterService } from 'src/app/services/router.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.scss']
})
export class SigninComponent {
  formForm!: FormGroup;
  loadingData = false
  message: string = '';
  success = false;
  err = false;
  constructor(private requestService: RequestService,
    private formBuilder: FormBuilder, public routerService: RouterService
  ) { }
  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
    this.formForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnSubmit() {
    this.loadingData = true;
    this.success = false
    this.err = false
    const username = this.formForm.get('username')?.value;
    const password = this.formForm.get('password')?.value;

    let data = {
      "username": username,
      "password": password,
    }

    console.log(data)

    this.requestService.post("https://mentor-me-7viu.onrender.com/api/login/", data).then(
      (response: any) => {
        console.log(response)
        this.message = response.message
        this.loadingData = false
        this.success = true
        this.err = false
        localStorage.setItem("user", JSON.stringify(response.data))
        if (response.is_mentor) {
          setTimeout(() => {
            this.routerService.routeRoute("/dashboard/mentor")
          }, 300)
        }
        if (response.is_mentee) {
          setTimeout(() => {
            this.routerService.routeRoute("/dashboard/mentee")
          }, 300)
        }
      }, (reason: any) => {
        this.loadingData = false
        this.message = "Login failed"
        this.success = false
        this.err = true
        console.log(reason)
      }
    )
  }


}
