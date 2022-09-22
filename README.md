# Authentication with cognito and gmail

In this application we will learn how to configure google app into AWS cognito. 

### Installation
- First you have to install aws sam cli into your machine. 
- Then configure aws cli.

**If you don't have CLI installed and configured into your local machine please follow prerequisite steps from this** [link](https://medium.com/@farzanajuthi08/how-to-make-an-application-using-serverless-application-model-sam-and-python-937415d38a44)

### Local Development

- After installation done, you have to pull the code from git repository [(HTTPS link)](https://github.com/farzana-juthi/authentication.git)
- Then go to project directory by using following command:
  ```
    cd auth
  ```
- Then open **template.yaml** file and change following (15-20) lines with appropriate data:
  - In line 15 (variable **CallBackUrlUserPoolClient**), you have to provide the url where google will be redirected after verifying user credential into google side. You can add multiple urls by comma separation. 
  - In line 16 (variable **LogOutUrlUserPoolClient**), you have to provide the url where cognito will be redirected after logout. You can add multiple url by comma separation.
  - In line 17 (variable **FIDGoogleClientId**), you have to give client id of google app. See [How to configure google app](https://medium.com/@farzanajuthi08/how-to-set-up-google-app-and-configure-amazon-cognito-for-social-sign-in-6844bc9bf605)
  - In line 18 (variable **FIDGoogleClientSecret**), you have to give secret client id of google app.
- Then give a project name into line 27. Here you have to set the value of the **ProjectName** parameter. Remember this data will be used to make domain name and domain name need to be unique.
  **You must have to change this value** 
- Then open terminal in root folder of this project and run following command:
  ```
    sam build
  ```
- If you deploy first time, then you have to run following command:
  ```
    sam deploy --guided --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
  ```
  If you want to run this command with your predefined profile then command will be 
  ```
    sam deploy --guided --profile <your_profile_name_without_this_bracket> --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
  ```
- After running previous command, you will see that you have to set a stack name. Please give a unique stack name.

  <img width="549" alt="step-1" src="https://user-images.githubusercontent.com/63281366/191643954-a022339c-cf22-4559-ac5b-3b24e87a671e.png">
  
  For example: I am giving stack name as auth-app.
  
  <img width="553" alt="step-2" src="https://user-images.githubusercontent.com/63281366/191644054-6166326d-dc32-42e6-88e8-6d9c2c40607d.png">


- Then click enter one after another until **SAM configuration environment** variable set to default value.
  
  <img width="766" alt="enter-untill-this" src="https://user-images.githubusercontent.com/63281366/191644374-499f5dd4-b120-46bd-8e3f-5183c37bb43b.png">

  
- Then wait for successful creation of cloudformation stack. 
- If you want to deploy after changes, then you need to build it first and run only deploy command like following:
  ```<img width="797" alt="output" src="https://user-images.githubusercontent.com/63281366/191654084-49cf256a-cb47-45ab-ace3-79b68ba31853.png">

    sam build
    sam deploy
  ```
- After successful deployment you will get some output. Save those for further implementation:
  
  <img width="737" alt="output" src="https://user-images.githubusercontent.com/63281366/191655785-6eb81fd5-0d4d-4fbb-9dc0-46669c4ba12d.png">

  ```
    DomainURL: It's value will be used as domain_url in frontend side
    CognitoAppClientID: It's value will be used as cognito_client_id in frontend side
    RootAPI: It's value will be used as base_url in frontend side
  ```

### Update Google APP - Authorized JavaScript origins and Authorized redirect URIs
- You must have to follow step 11 of this [link](https://medium.com/@farzanajuthi08/how-to-set-up-google-app-and-configure-amazon-cognito-for-social-sign-in-6844bc9bf605)


### Now you have to use cognito and created APIs into your frontend side

  To start implementing it into code, check the flow from diagram:

  ![auth_implementation_flow](https://user-images.githubusercontent.com/63281366/191645091-4c860761-b4dd-4a5a-9fb6-b989bcb2a222.jpg)


- First make the url which will be used in **Sign In with gmail** button.
  ```
    <domain_url>/oauth2/authorize?identity_provider=Google&redirect_uri=<frontend_redirect_url>&response_type=CODE&client_id=<cognito_client_id>&scope=email openid profile aws.cognito.signin.user.admin
  ``` 
  - Change curly bracket variables value like following
      - **domain_url**: https://learning-auth-auth-stack-dev.auth.us-west-2.amazoncognito.com
      - **frontend_redirect_url**: Remember this url is very important. It is used in cognito side as UserPoolClientCallBackUrlDevAndProd. If this url not match then you will get redirect mismatch error.
                                   Here my redirect url is http://localhost:4200/dashboard/
      - **cognito_client_id**: Just check nested stack output from aws console and variable name is NestedCognitoUserPoolClientId. Here my client id is 7vfokrcbq7tc7s3u35qhj2054h
    
  ```
    Example: https://learning-auth-auth-stack-dev.auth.us-west-2.amazoncognito.com/oauth2/authorize?identity_provider=Google&redirect_uri=http://localhost:4200/dashboard/&response_type=CODE&client_id=7vfokrcbq7tc7s3u35qhj2054h&scope=email openid profile aws.cognito.signin.user.admin
  ```
- Then this url will take you to google sign in page. Here you have to give your sign in email and password. If google verifies that credentials are right then it will redirect your to your application with a code.
    
  ```
    Example: http://localhost:4200/dashboard?code=09266419-d8b9-4005-8830-3bc57255c802
  ```
- After that you have to call internally another url with following information to get tokens information.
  - This will be a post method. Parameters need to pass along with the url are:
      
      Method: POST
      
      URL: <domain_url>/oauth2/token
      
      Example: https://learning-auth-auth-stack-dev.auth.us-west-2.amazoncognito.com/oauth2/token
      
      Parameters:
  ```
      {
        grant_type: "authorization_code",
        client_id: "Here you have to pass cognito_client_id what you have given into first step",
        code: "Code you have got into the last step",
        redirect_uri: "Here you have to give redirected url what you have given into first step"
      }
  ```    

  ```
      Example:
      {
        grant_type: "authorization_code",
        client_id: "7vfokrcbq7tc7s3u35qhj2054h",
        code: "09266419-d8b9-4005-8830-3bc57255c802",
        redirect_uri: "http://localhost:4200/dashboard/"
      }
  ```
- Then you can get social sign in related data by calling following API
  - Method: POST
  - URL: https://<base_url><path>
  
  Example: https://joc4u21r8e.execute-api.us-west-2.amazonaws.com/dev/auth/authentication/social-signin  
    - API base url: https://joc4u21r8e.execute-api.us-west-2.amazonaws.com/dev
    - Path: /auth/authentication/social-signin
  - Parameter: 
    {
       "id_token": "",
       "access_token": "",
       "refresh_token": "",
       "expires_in": "",
       "token_type": ""
    }
  
  ```
  {
    "id_token": "",
    "access_token": "",
    "refresh_token": "",
    "expires_in": "",
    "token_type": ""
  }

  ```
- If you want to log-out, then you have to call logout API
  - Method: POST
  - URL: <base_url><path>
  
    Example: https://joc4u21r8e.execute-api.us-west-2.amazonaws.com/dev/auth/authentication/social-signin  
    - API base url: https://joc4u21r8e.execute-api.us-west-2.amazonaws.com/dev
    - Path: /auth/authentication/global-logout
  - Parameter: {"access_token": ""}
  ```
  {
   "access_token":"Here you have to pass access token "
  }

  ```

  

