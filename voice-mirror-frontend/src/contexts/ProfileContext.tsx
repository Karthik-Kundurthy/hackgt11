import { createContext } from "react";
import { Profile } from "../models/Profile";
import { Persona } from "../models/Persona";

interface ProfileContextInformation {
  profile: Profile | undefined;
  handleLogin: (name: string, password: string) => Promise<void>;
  personas: Persona[];
}
export const ProfileContext = createContext<ProfileContextInformation>({
  profile: undefined,
  handleLogin: async (name: string, password: string) => {},
  personas: [],
});