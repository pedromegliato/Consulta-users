export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  phone: string | null;
}

export interface FetchUsersResult {
  users: User[];
  failed: number[];
}
