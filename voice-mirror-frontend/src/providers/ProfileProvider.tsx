import { ProfileContext } from "../contexts/ProfileContext";
import { Profile } from "../models/Profile";
import { Persona } from "../models/Persona";
import { useState } from "react";
import avatar from "../assets/avatar.png";
import { login } from "../api/api";

export default function ProfileProvider({ children }: any) {
  const [profile, setProfile] = useState<Profile | undefined>(undefined);
  const [personas, setPersonas] = useState<Persona[]>([ 
    {
      id: "1",
      image: avatar,
      name: "Harish Kanthi",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat, molestie ipsum et, eleifend nunc",
    },
  ]);

  const handleLogin = async (username: string, password: string) => {
    const response = await login(username, password);
    if (response.error) {
      alert(response.data);
    } else {
      localStorage.setItem("token", response.data.access_token);
      setProfile({ username: username });
    }
  };

  return (
    <ProfileContext.Provider
      value={{
        profile: profile,
        personas: personas,
        handleLogin: handleLogin,
      }}
    >
      {children}
    </ProfileContext.Provider>
  );
}
