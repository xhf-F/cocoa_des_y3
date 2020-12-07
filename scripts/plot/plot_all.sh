for NAME in $(find . -mindepth 1 -maxdepth 1 -type d); do
  declare NAME2=$(echo "${NAME}" | sed -E 's@./@@')
  cd ./$NAME2
  source plot_all.sh &
  cd ../
done