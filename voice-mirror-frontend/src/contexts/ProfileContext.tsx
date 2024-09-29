import { createContext } from "react";
import { Profile } from "../models/Profile";
import { Persona } from "../models/Persona";

interface ProfileContextInformation {
  profile: Profile | undefined;
  handleLogin: (username: string, password: string) => Promise<void>;
  personas: Persona[];
}
export const ProfileContext = createContext<ProfileContextInformation>({
  profile: undefined,
  handleLogin: async (username: string, password: string) => {},
  personas: [],
});
