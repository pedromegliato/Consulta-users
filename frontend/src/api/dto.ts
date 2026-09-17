export interface FetchUsersRequestDto {
  user_ids: number[];
}

export interface UserDto {
  id: number;
  name: string;
  username: string;
  email: string;
  phone: string | null;
}

export interface FetchUsersResponseDto {
  users: UserDto[];
  failed: number[];
}

export interface UserPageDto {
  items: UserDto[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ApiErrorDto {
  error: {
    code: string;
    message: string;
    details: string[];
    request_id: string;
  };
}
