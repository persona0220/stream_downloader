#!/bin/bash

find . -type f  | xargs -I{} sh -c 'mv -v $0 ${0/*_/0}' {} ;

ls ??.ts | xargs -I{} sh -c 'mv -v $0 000${0}' {} ;
ls ???.ts | xargs -I{} sh -c 'mv -v $0 00${0}' {} ;
ls ????.ts | xargs -I{} sh -c 'mv -v $0 0${0}' {} ;
