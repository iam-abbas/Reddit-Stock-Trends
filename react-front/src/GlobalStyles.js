import { createGlobalStyle } from "styled-components/macro";

export default createGlobalStyle`

* {
    box-sizing: border-box;
    
}

body {
    
    margin: 0;
    font-size: 100%;
    background-color: var(--surface-a);
    font-family: 'Helvetica Neue', sans-serif;

}

a {
    color: white;
}
:root {
    --surface-a: #1f2d40;
    }
`;
