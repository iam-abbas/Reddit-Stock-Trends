import { createGlobalStyle } from "styled-components/macro";

export default createGlobalStyle`

* {
    box-sizing: border-box;
    font-family: 'BaiJamjuree';
}

body {
    
    margin: 0;
    font-size: 112.5%;
    background-color: var(--surface-a);
    font-family: var(--bs-font-sans-serif);
}

:root {
    --surface-a: #1f2d40;
--bs-font-sans-serif: system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
--bs-font-monospace: SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
--bs-gradient: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0));
    }
`;
