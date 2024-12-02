export interface NavbarProps {
  isOpen?: boolean;
  toggleMenu?: () => void;
}

export interface CoverLetterFormData {
  email: string;
  cvFile: File | null;
  jobAdOption: 'link' | 'upload' | 'freeform';
  jobAdLink: string;
  jobAdFile: File | null;
  jobAdText: string;
  backgroundText: string;
}

export interface JobMatcherFormData {
  email: string;
  cvFile: File | null;
  jobPreferences: string;
  fylke: string;
  kommuneBydel: string;
}

export interface LocationData {
  [key: string]: string[];
}

export interface TextAreaEvent extends React.ChangeEvent<HTMLTextAreaElement> {
  target: HTMLTextAreaElement;
}

export interface SelectEvent extends React.ChangeEvent<HTMLSelectElement> {
  target: HTMLSelectElement;
}

export interface InputEvent extends React.ChangeEvent<HTMLInputElement> {
  target: HTMLInputElement;
}

export interface ApiError {
  message: string;
  status?: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
  message?: string;
}