export interface AppHeaderProps {
  activeMenuItem: string;
  historyPush: (value: string) => void;
  logout: () => void;
  role: string | null;
}
