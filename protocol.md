RequestOrResponse => Size (RequestMessage | ResponseMessage)
  Size => int32
    
Request Header v1 => request_api_key request_api_version correlation_id client_id 
  request_api_key => INT16
  request_api_version => INT16
  correlation_id => INT32
  client_id => NULLABLE_STRING
   
Response Header v1 => correlation_id TAG_BUFFER 
  correlation_id => INT32

ApiVersions Response (Version: 2) => error_code [api_keys] throttle_time_ms 
  error_code => INT16
  api_keys => api_key min_version max_version 
    api_key => INT16
    min_version => INT16
    max_version => INT16
  throttle_time_ms => INT32



ARRAY	Represents a sequence of objects of a given type T. Type T can be either a primitive type (e.g. STRING) or a structure. First, the length N is given as an INT32. Then N instances of type T follow. A null array is represented with a length of -1. In protocol documentation an array of T instances is referred to as [T].