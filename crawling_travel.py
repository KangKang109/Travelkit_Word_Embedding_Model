import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import nltk
import re
from urllib.parse import urljoin
from collections import deque

nltk.download('punkt')

# 크롤링할 시드 URL 설정
seed_url = "https://www.google.com/search?q=%ED%95%B4%EC%99%B8%EC%97%AC%ED%96%89&sca_esv=c744cb070de47b7e&sxsrf=ADLYWILyEAFR34OZK9E52blOLsr2rj_4xQ%3A1732539846981&ei=xnVEZ7zSO4HAvr0Ptd6FiAo&ved=0ahUKEwi8zY3xxfeJAxUBoK8BHTVvAaEQ4dUDCA8&uact=5&oq=%ED%95%B4%EC%99%B8%EC%97%AC%ED%96%89&gs_lp=Egxnd3Mtd2l6LXNlcnAiDO2VtOyZuOyXrO2WiTIKECMYgAQYJxiKBTIKECMYgAQYJxiKBTIEECMYJzIKEAAYgAQYQxiKBTILEAAYgAQYsQMYgwEyBRAAGIAEMgUQABiABDIKEAAYgAQYQxiKBTIFEAAYgAQyBRAAGIAESNEJUABY7QdwBHgBkAEEmAHWAaABqAqqAQYwLjEwLjG4AQPIAQD4AQGYAgegAtACwgIQEAAYgAQYsQMYgwEYFBiHAsICCxAuGIAEGLEDGIMBwgIKEAAYgAQYFBiHApgDAJIHAzQuM6AH2YAB&sclient=gws-wiz-serp"
#seed_url = "https://www.google.co.kr/search?q=%EB%8F%99%EC%9C%A0%EB%9F%BD+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=1af2431bf3667efc&sxsrf=ADLYWIKQLjg8e4jjUlCahMp95pEk-ZcRNg%3A1732454120274&ei=6CZDZ5OzEMjh2roP9_iqiAQ&oq=%EB%8F%99%EC%9C%A0%EB%9F%BD&gs_lp=Egxnd3Mtd2l6LXNlcnAiCeuPmeycoOufvSoCCAAyChAAGIAEGEMYigUyBRAAGIAEMgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyCBAuGIAEGLEDMgUQABiABEitZVAAWLJRcAR4AZABApgBxQGgAe4LqgEEMC4xMrgBA8gBAPgBAZgCCaAC9ASoAhDCAgoQIxiABBgnGIoFwgIEECMYJ8ICBBAAGAPCAggQABiABBixA8ICBBAuGAPCAg4QLhiABBixAxjRAxjHAcICERAuGIAEGLEDGNEDGIMBGMcBwgILEAAYgAQYsQMYgwHCAgsQLhiABBjRAxjHAcICBxAjGCcY6gLCAhQQABiABBjjBBi0AhjpBBjqAtgBAcICCxAuGIAEGLEDGIMBmAMJugYGCAEQARgBkgcDNC41oAf7kgE&sclient=gws-wiz-serp"
#seed_url = "http://www.besttour.co.kr/"
#seed_url = "https://www.joongang.co.kr/travel/news"
#seed_url = "https://www.traveltimes.co.kr/"
#seed_url = "https://www.joongang.co.kr/travel/abroad"
#seed_url ="https://www.yna.co.kr/culture/travel-leisure"
#seed_url = "http://www.travelinfo.co.kr/main/main.html"
#seed_url = "https://www.gtn.co.kr/"
#seed_url = "https://www.traveltimes.co.kr/"
#seed_url = "https://www.google.com/search?q=%ED%8F%AC%EB%A5%B4%ED%88%AC%EA%B0%88+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWII-lZYtU0fN24ENFeeGl5AuHkx9PA%3A1732293924568&ei=JLVAZ5SsIuyO2roP_8POkQk&ved=0ahUKEwiUzpTgsfCJAxVsh1YBHf-hM5IQ4dUDCA8&uact=5&oq=%ED%8F%AC%EB%A5%B4%ED%88%AC%EA%B0%88+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egxnd3Mtd2l6LXNlcnAiHe2PrOultO2IrOqwiCDsl6ztlokg7KSA67mE66y8MgUQABiABDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIGEAAYBRgeSNtKUI4JWItJcAh4AZABBJgBigGgAYsQqgEEMC4xN7gBA8gBAPgBAZgCDKACjgTCAgoQABiwAxjWBBhHwgIGEAAYBxgewgIIEAAYBxgIGB7CAgoQIxiABBgnGIoFwgIEECMYJ8ICChAAGIAEGBQYhwLCAgQQABgewgIHECMYsAIYJ8ICBxAAGIAEGA3CAggQABgFGA0YHsICCBAAGAUYBxgemAMAiAYBkAYKkgcDOC40oAeqVg&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?q=%ED%8C%8C%EB%A6%AC+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIKRke4od8-LyvhBKDYKP5Cntueulg%3A1732293833413&ei=ybRAZ570GLfc2roPkt2UwAE&ved=0ahUKEwje_Ni0sfCJAxU3rlYBHZIuBRgQ4dUDCA8&uact=5&oq=%ED%8C%8C%EB%A6%AC+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egxnd3Mtd2l6LXNlcnAiF-2MjOumrCDsl6ztlokg7KSA67mE66y8MgUQABiABDIGEAAYCBgeMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMgYQABgFGB5I1QRQAFiAA3ABeAGQAQKYAbEBoAHLBKoBAzEuNLgBA8gBAPgBAZgCAaACBZgDAJIHATGgB5UU&sclient=gws-wiz-serp"
#seed_url ="https://www.google.com/search?q=%EB%B2%A0%ED%8A%B8%EB%82%A8+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIJ7XGN0gR5yM4RZbHYMorB34snKEQ%3A1732293823503&ei=v7RAZ_qsHovd2roP4I7emAk&ved=0ahUKEwi6iPyvsfCJAxWLrlYBHWCHF5MQ4dUDCA8&uact=5&oq=%EB%B2%A0%ED%8A%B8%EB%82%A8+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egxnd3Mtd2l6LXNlcnAiGuuyoO2KuOuCqCDsl6ztlokg7KSA67mE66y8MgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgYQABgIGB4yBhAAGAgYHjIGEAAYBRgeMgYQABgFGB5I3h9QtBVYlh5wBHgBkAECmAGMAaABiwmqAQQwLjEwuAEDyAEA-AEBmAIIoALdA8ICChAAGLADGNYEGEfCAgoQABiABBgUGIcCwgIKEAAYgAQYQxiKBcICBBAAGB6YAwCIBgGQBgqSBwM0LjSgB-Q-&sclient=gws-wiz-serp" 
#seed_url = "https://www.google.com/search?q=%EC%BA%90%EB%A6%AC%EC%96%B4%EC%8B%B8%EA%B8%B0&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIKQZIRrCvIFRrF4CFcaGA-RovWU2Q%3A1732293211384&ei=W7JAZ-CQF4_q1e8P87PpqAc&ved=0ahUKEwigqouMr_CJAxUPdfUHHfNZGnUQ4dUDCA8&uact=5&oq=%EC%BA%90%EB%A6%AC%EC%96%B4%EC%8B%B8%EA%B8%B0&gs_lp=Egxnd3Mtd2l6LXNlcnAiD-y6kOumrOyWtOyLuOq4sDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBEivCVCeBFjiB3ADeAGQAQKYAYUBoAHjBKoBAzAuNbgBA8gBAPgBAZgCBaACgQLCAgoQABiwAxjWBBhHwgIFEAAYgASYAwCIBgGQBgqSBwMzLjKgB88L&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?q=%EA%B0%80%EB%B0%A9%EC%8B%B8%EA%B8%B0&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIL1NxcMKHByb6X-4nuEQ4AtuyY1Mg%3A1732293100093&ei=7LFAZ_61Bd2o1e8PnOeiqQk&ved=0ahUKEwj-24LXrvCJAxVdVPUHHZyzKJUQ4dUDCA8&uact=5&oq=%EA%B0%80%EB%B0%A9%EC%8B%B8%EA%B8%B0&gs_lp=Egxnd3Mtd2l6LXNlcnAiDOqwgOuwqeyLuOq4sDIFEAAYgAQyBhAAGAUYHjIGEAAYBRgeMgYQABgFGB4yBhAAGAUYHjIGEAAYBRgeSKEIUKkDWOMGcAN4AZABAZgBd6ABsASqAQMwLjW4AQPIAQD4AQGYAgWgAuoBwgIKEAAYsAMY1gQYR8ICBRAuGIAEwgIKEAAYgAQYQxiKBcICBhAAGAoYHsICBBAAGB7CAggQABiABBiiBJgDAIgGAZAGCpIHAzMuMqAHxRU&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?q=%EB%AC%BC%EA%B1%B4&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIJovRccQEgJluRBTvvkSDLXGrnuHw%3A1732292926449&ei=PrFAZ7KTG42Tvr0PoPeEkAc&ved=0ahUKEwiyqpyErvCJAxWNia8BHaA7AXIQ4dUDCA8&uact=5&oq=%EB%AC%BC%EA%B1%B4&gs_lp=Egxnd3Mtd2l6LXNlcnAiBuusvOqxtDIKEAAYgAQYFBiHAjIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEj_FlCuBFj_EXAIeAGQAQSYAYwBoAHRCqoBBDAuMTG4AQPIAQD4AQGYAgygArEEqAITwgIHECMYsAMYJ8ICChAAGLADGNYEGEfCAgcQIxgnGOoCwgIUEAAYgAQY4wQYtAIY6QQY6gLYAQHCAgoQIxiABBgnGIoFwgILEAAYgAQYsQMYgwHCAgQQABgDwgIFEC4YgATCAgcQABiABBgNwgIFECEYoAGYAwiIBgGQBgq6BgYIARABGAGSBwM4LjSgB49n&sclient=gws-wiz-serp"
#seed_url ="https://www.google.com/search?q=%EA%B5%AD%EB%82%B4&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIJ7_vsFdUhUUaJM37eaNpjranORng%3A1732292848702&ei=8LBAZ_nNKuGzvr0PlvXpqQs&ved=0ahUKEwj5hZPfrfCJAxXhma8BHZZ6OrUQ4dUDCA8&uact=5&oq=%EA%B5%AD%EB%82%B4&gs_lp=Egxnd3Mtd2l6LXNlcnAiBuq1reuCtDIKECMYgAQYJxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIEEAAYAzIKEAAYgAQYQxiKBTIKEAAYgAQYFBiHAjIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTILEAAYgAQYsQMYgwFI-AhQAFi1BHABeAGQAQCYAZABoAHUBaoBAzAuNrgBA8gBAPgBAZgCBKAC4QLCAgQQIxgnwgIREC4YgAQYsQMY0QMYgwEYxwHCAggQABiABBixA8ICCxAuGIAEGNEDGMcBwgIQEAAYgAQYsQMYgwEYFBiHAsICBRAAGIAEmAMAkgcDMS4zoAeMQQ&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?q=%ED%95%B4%EC%99%B8&sca_esv=f906251265b5c9a0&biw=851&bih=931&sxsrf=ADLYWIJ18qnexKTkWYPC1jvYD_EoaxH5Lg%3A1732292759967&ei=l7BAZ8LcOrGX0-kPxeOq2Ao&ved=0ahUKEwiChOu0rfCJAxWxyzQHHcWxCqsQ4dUDCA8&uact=5&oq=%ED%95%B4%EC%99%B8&gs_lp=Egxnd3Mtd2l6LXNlcnAiBu2VtOyZuDIKECMYgAQYJxiKBTIEECMYJzIKECMYgAQYJxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBUirEFDQCVjdDnAEeAGQAQKYAYUBoAHTBaoBAzAuNrgBA8gBAPgBAZgCB6ACjAOoAhLCAgcQIxgnGOoCwgIUEAAYgAQY4wQYtAIY6QQY6gLYAQHCAgoQABiABBgUGIcCwgIEEAAYA8ICBRAAGIAEwgIFEC4YgATCAgsQLhiABBixAxjUAsICCBAAGIAEGLEDwgILEAAYgAQYsQMYgwGYAwu6BgYIARABGAGSBwM0LjOgB8NQ&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?sca_esv=f906251265b5c9a0&sxsrf=ADLYWIJuIdOvNMytg0GkUXXPfX3LLuwVow:1732292748782&q=%EA%B5%AD%EB%82%B4%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sa=X&ved=2ahUKEwi6rsCvrfCJAxUJlFYBHQS8Ks0Q1QJ6BAg5EAE&biw=851&bih=931&dpr=1.5"
#seed_url = "https://www.google.com/search?q=%EC%97%AC%ED%96%89&sca_esv=396436077eb24e00&hl=ko&biw=851&bih=931&sxsrf=ADLYWIKyik3bR2FVrrYAyeZ_fCIaPC2DhQ%3A1732291471260&ei=j6tAZ-HJD_fl2roP5uCJuQM&ved=0ahUKEwihzarOqPCJAxX3slYBHWZwIjcQ4dUDCA8&uact=5&oq=%EC%97%AC%ED%96%89&gs_lp=Egxnd3Mtd2l6LXNlcnAiBuyXrO2WiTIKECMYgAQYJxiKBTIEECMYJzIKECMYgAQYJxiKBTINEAAYgAQYsQMYFBiHAjIREC4YgAQYsQMYgwEYxwEYrwEyDRAAGIAEGLEDGBQYhwIyChAAGIAEGEMYigUyChAAGIAEGEMYigUyCBAAGIAEGLEDMggQABiABBixA0j7T1CQJ1iFTnAFeAGQAQWYAagBoAGcEqoBBDEuMTa4AQPIAQD4AQGYAgegArwCwgIKEAAYsAMY1gQYR8ICBxAjGLACGCfCAgcQABiABBgNwgIGEAAYBxgewgIFEAAYgATCAggQABgHGAgYHsICCBAAGIAEGKIEwgIIEAAYBRgHGB7CAgQQABgewgIGEAAYCBgewgIGEAAYBRgewgIKEAAYgAQYFBiHAsICCxAAGIAEGLEDGIMBwgIEEC4YA5gDAIgGAZAGCpIHAzUuMqAHjpsB&sclient=gws-wiz-serp"
#seed_url = "https://www.google.com/search?q=%EB%AF%B8%EA%B5%AD+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=396436077eb24e00&hl=ko&biw=851&bih=931&sxsrf=ADLYWIIFfMxqLsmnKGAs2VDHrKO_Gj_TSA%3A1732291379253&ei=M6tAZ-GWD8_g2roP9KGokA0&ved=0ahUKEwih_LqiqPCJAxVPsFYBHfQQCtIQ4dUDCA8&uact=5&oq=%EB%AF%B8%EA%B5%AD+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egxnd3Mtd2l6LXNlcnAiF-uvuOq1rSDsl6ztlokg7KSA67mE66y8MgoQABiABBhDGIoFMgYQABgHGB4yBhAAGAcYHjIFEAAYgAQyBRAAGIAEMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHkijPFCwB1jVOnADeAGQAQOYAZsBoAHjCKoBAzAuObgBA8gBAPgBAZgCBaACgQLCAgoQABiwAxjWBBhHwgIKECMYgAQYJxiKBcICBBAjGCeYAwCIBgGQBgqSBwMzLjKgB5RA&sclient=gws-wiz-serp"
#seed_url ="https://www.google.co.kr/search?q=%EC%95%84%EC%8B%9C%EC%95%84+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=396436077eb24e00&sxsrf=ADLYWIIHRSZLzGanIb0w-01ZN2kPUhQNRw%3A1732291398301&source=hp&ei=RqtAZ_e1EOCQvr0P4dOL6Qc&iflsig=AL9hbdgAAAAAZ0C5Vh20GyBIE1el78N5LP7utC8CJSfC&ved=0ahUKEwj38MOrqPCJAxVgiK8BHeHpIn0Q4dUDCBg&uact=5&oq=%EC%95%84%EC%8B%9C%EC%95%84+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egdnd3Mtd2l6IhrslYTsi5zslYQg7Jes7ZaJIOykgOu5hOusvDIEECMYJzIIEAAYBRgNGB4yCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBEidE1D_A1jpEXAGeACQAQWYAY4BoAH-E6oBBDAuMjK4AQPIAQD4AQGYAg2gAsMGqAIKwgIHECMYJxjqAsICChAjGIAEGCcYigXCAgoQABiABBgUGIcCwgILEAAYgAQYsQMYgwHCAhEQLhiABBixAxjRAxiDARjHAcICCxAuGIAEGLEDGIMBwgIKEAAYgAQYQxiKBcICFhAuGIAEGLEDGNEDGIMBGBQYhwIYxwHCAg4QLhiABBixAxjRAxjHAcICCBAAGIAEGLEDwgIFEAAYgATCAgQQABgDwgIFEC4YgATCAgYQABgFGB6YAwaSBwM2LjegB-3BAQ&sclient=gws-wiz"
#seed_url ="https://www.google.com/search?q=%EC%9C%A0%EB%9F%BD+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=396436077eb24e00&hl=ko&biw=851&bih=931&sxsrf=ADLYWILSKGC4eQdNZdTULsgXb5RD6UX74w%3A1732291245210&ei=rapAZ5_EDLmAvr0P-cnu8QM&ved=0ahUKEwjfzsXip_CJAxU5gK8BHfmkOz4Q4dUDCA8&uact=5&oq=%EC%9C%A0%EB%9F%BD+%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egxnd3Mtd2l6LXNlcnAiF-ycoOufvSDsl6ztlokg7KSA67mE66y8MgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBhAAGAcYHjIFEAAYgAQyBhAAGAcYHjIFEAAYgAQyBhAAGAcYHjIGEAAYBxgeMgYQABgHGB5Ixw5Q2AdYyQtwAngBkAEBmAGMAaAB8AWqAQMwLja4AQPIAQD4AQGYAgSgApECwgIHECMYsAMYJ8ICChAAGLADGNYEGEeYAwCIBgGQBgqSBwMyLjKgB7Er&sclient=gws-wiz-serp"
#seed_url ="https://www.google.com/search?q=%ED%95%B4%EC%99%B8%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=396436077eb24e00&hl=ko&sxsrf=ADLYWIL_mAYbQp9Pg2FFI0JfC_Ph6CXXTQ:1732290859679&ei=K6lAZ4SYKbCn1e8PvKj1wAo&start=100&sa=N&sstk=ATObxK5gjbm40CEYPbYrZAFDAzUTbnimrbE9KRZlxBrTnlq3V05X5hu1wI_XO40zRdSm6w87M8ZUGBViLCEsEpuqeI6grMyDf_8AZ3Rykcbd9_4XroSuxiEM5wHl7OA9D2IF&ved=2ahUKEwjE2dqqpvCJAxWwU_UHHTxUHag4WhDy0wN6BAgKEA8&biw=851&bih=931&dpr=1.5"
#seed_url ="https://www.google.com/search?q=%ED%95%B4%EC%99%B8%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&sca_esv=396436077eb24e00&hl=ko&sxsrf=ADLYWIL35rwBIMooifZBXfP9PAHMwy9orA%3A1732290765202&source=hp&ei=zahAZ-X0Ce3bvr0PyuDa6Qs&iflsig=AL9hbdgAAAAAZ0C23TlExBS89uuSzMvEKnjBOXsOd3Qw&ved=0ahUKEwilj9L9pfCJAxXtra8BHUqwNr0Q4dUDCBg&uact=5&oq=%ED%95%B4%EC%99%B8%EC%97%AC%ED%96%89+%EC%A4%80%EB%B9%84%EB%AC%BC&gs_lp=Egdnd3Mtd2l6IhbtlbTsmbjsl6ztlokg7KSA67mE66y8MgoQIxiABBgnGIoFMgQQIxgnMgoQIxiABBgnGIoFMgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyChAAGIAEGBQYhwJIgRZQvQRYsxRwBngAkAEFmAGqAaABwBaqAQQwLjIwuAEDyAEA-AEBmAIMoAKZB6gCCsICBxAjGCcY6gLCAgQQABgDwgIFEC4YgATCAgsQLhiABBixAxjUAsICCBAAGIAEGLEDwgILEAAYgAQYsQMYgwGYAwiSBwM2LjagB4PhAQ&sclient=gws-wiz"

# 텍스트 파일 저장 경로
file_path = 'C:\\Users\\minwo\\Documents\\word2vec\\crawled_data.txt'

# 크롤링할 최대 페이지 수 (예시로 설정)
max_pages = 30

# URL 큐 (FIFO 방식)
url_queue = deque([seed_url])

# 방문한 URL을 추적하기 위한 집합
visited_urls = set()

# 전체 토큰 수
total_tokens = 0

# 페이지 수 카운트
page_count = 0

while url_queue and page_count < max_pages:
    # 큐에서 URL 하나 꺼내기
    current_url = url_queue.popleft()

    if current_url in visited_urls:
        continue  # 이미 방문한 URL이면 건너뛰기

    # 웹 페이지 요청 및 HTML 파싱
    try:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 본문 추출 (실제 사이트에 맞는 태그로 수정)
        article = soup.find('div', {'class': 'article-content'})  # 이 부분은 사이트에 맞게 수정
        if article:
            text = article.get_text()
        else:
            text = soup.get_text()

        # 한글만 남기고 나머지 문자(특수문자, 영어 등) 제거
        text = re.sub(r'[^ㄱ-ㅎ가-힣\s]', '', text)

        # 텍스트 토큰화
        tokens = word_tokenize(text)
        corpus_size = len(tokens)
        total_tokens += corpus_size

        # 텍스트 파일에 추가
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(text)

        # 출력
        print(f"{current_url}에서 크롤링된 텍스트가 {file_path}에 추가되었습니다!")
        print(f"추출된 말뭉치 개수: {corpus_size}개")

        # 방문한 URL 추가
        visited_urls.add(current_url)

        # 링크 추출 (현재 페이지에서 다른 링크를 찾고 큐에 추가)
        for link in soup.find_all('a', href=True):
            # 상대 URL을 절대 URL로 변환
            full_url = urljoin(current_url, link['href'])
            if full_url not in visited_urls:
                url_queue.append(full_url)

        # 페이지 수 증가
        page_count += 1

    except Exception as e:
        print(f"URL 크롤링 중 오류 발생: {current_url}, 오류: {e}")

# 크롤링이 완료된 후 총 말뭉치 개수 출력
print(f"총 크롤링된 말뭉치 개수: {total_tokens}개")
# 크롤링이 완료된 후 텍스트 파일 내 총 말뭉치 개수 출력
with open(file_path, 'r', encoding='utf-8') as f:
    file_text = f.read()  # 파일에서 텍스트 읽기
    file_tokens = word_tokenize(file_text)  # 텍스트를 다시 토큰화
    file_corpus_size = len(file_tokens)  # 말뭉치 개수

# 최종 출력
print(f"총 크롤링된 말뭉치 개수: {total_tokens}개")
print(f"텍스트 파일 내 총 말뭉치 개수: {file_corpus_size}개")
