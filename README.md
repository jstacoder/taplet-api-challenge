##image upload/view api

### api endpoints:  
  + `/api/v1/upload` 
    - method: POST
    - args: 
      * `user_id` - int - required
      * `group_id` - int - required
      * `image_url` - string - required

  + `/api/v1/list`
  + `/api/v1/list/<group_id>`
    - method: GET
    - args:        
      * `group_id` - int - optional


  + `/api/v1/view/<image_id>`
    - method: GET
    - args:
      * `image_id` - int - required

  + `/api/v1/stream`
  + `/api/v1/stream/<group_id>`
    - method: GET
    - args:
      * `group_id` - int - optional
